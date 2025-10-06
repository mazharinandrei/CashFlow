from decimal import Decimal

from django import forms
from django.utils.timezone import localdate

from categories.models import Category
from statuses.models import Status
from subcategories.models import Subcategory
from transaction_types.models import Type
from transactions.models import Transaction


def validate_input(input_value):
    try:
        return int(input_value)
    except ValueError:
        pass


class TransactionFormMixin(forms.ModelForm):
    """
    Форма, содержащая общие поля для форм записи: Статус, Тип, Категорию, Подкатегорию.
    """
    status = forms.ModelChoiceField(queryset=Status.objects.none(),
                                    label="Статус")

    type = forms.ModelChoiceField(queryset=Type.objects.none(),
                                  label="Тип",
                                  widget=forms.Select(attrs={
                                      "hx-get": "/categories/get-options",
                                      "hx-target": "#category",
                                      "hx-swap": "innerHTML",
                                      "hx-trigger": "input changed load",
                                      "hx-on::after-request":
                                          "if (this.value === '') "
                                          "{document.getElementById('subcategory').disabled = true; "
                                          "document.getElementById('category').disabled = true;}"
                                          "else {document.getElementById('subcategory').disabled = true; document.getElementById('category').disabled = false;}"
                                          "document.getElementById('subcategory').innerHTML = ''; "
                                  }))

    category = forms.ModelChoiceField(queryset=Category.objects.none(),
                                      label="Категория",
                                      widget=forms.Select(attrs={
                                          "disabled": True,
                                          "id": "category",
                                          "hx-get": "/subcategories/get-options",
                                          "hx-target": "#subcategory",
                                          "hx-swap": "innerHTML",
                                          "hx-trigger": "input changed load",
                                          "hx-on::after-request":
                                              "if (this.value ==='')"
                                              "{document.getElementById('subcategory').disabled = true;}"
                                              "else {document.getElementById('subcategory').disabled = false;}"
                                      }))

    subcategory = forms.ModelChoiceField(queryset=Subcategory.objects.none(),
                                         label="Подкатегория",
                                         widget=forms.Select(attrs={"id": "subcategory",
                                                                    "disabled": True}))

    def set_selects(self, category_enable=None, subcategory_enable=None):
        if category_enable is not None:
            self.fields["category"].widget.attrs["disabled"] = not category_enable
        if subcategory_enable is not None:
            self.fields["subcategory"].widget.attrs["disabled"] = not subcategory_enable

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        # добавляем в поля объекты пользователя
        self.fields["status"].queryset = Status.objects.filter(created_by=user)
        self.fields["type"].queryset = Type.objects.filter(created_by=user)

        if self.instance.pk:
            """
            если обновляем существующий объект
            """
            self.fields["category"].queryset = Category.objects.filter(
                type=self.instance.subcategory.category.type)
            self.fields["subcategory"].queryset = Subcategory.objects.filter(
                category=self.instance.subcategory.category)

            # так как модель не хранит category и type, их нужно восстанавливать
            self.fields["category"].initial = self.instance.subcategory.category
            self.fields["type"].initial = self.instance.subcategory.category.type

            self.set_selects(category_enable=True, subcategory_enable=True)

        if self.data:
            """
            если отправляем данные с формы
            """

            if self.data.get("type"):
                validated_type = validate_input(self.data.get("type"))
                self.fields["category"].queryset = Category.objects.filter(
                    type=validated_type)
                self.set_selects(category_enable=True)
            else:
                self.set_selects(False, False)

            if self.data.get("category"):
                validated_category = validate_input(self.data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(
                    category=validated_category)
                self.set_selects(category_enable=True, subcategory_enable=True)
            else:
                self.set_selects(subcategory_enable=False)


class TransactionsFilterForm(TransactionFormMixin, forms.ModelForm):
    """
    Форма для фильтрации на главной странице
    """

    class Meta:
        model = Transaction
        fields = ("status", "type", "category", "subcategory")

    date_from = forms.DateField(label="Начало диапазона",
                                required=False,
                                widget=forms.DateInput(attrs={"type": "date"}))

    date_to = forms.DateField(label="Конец диапазона",
                              required=False,
                              widget=forms.DateInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):  # Отключаем обязательность полей
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class TransactionModelForm(TransactionFormMixin, forms.ModelForm):
    class Meta:
        model = Transaction
        fields = "__all__"

    # Изменяем порядок полей, так как добавляем в форму поля, не связанные с моделью (тип, категория)
    field_order = ["created_at", "status", "type", "category", "subcategory", "amount", "description"]

    created_at = forms.DateField(label="Дата записи",
                                 widget=forms.DateInput(attrs={"type": "date"},
                                                        format='%Y-%m-%d'),
                                 initial=localdate().strftime('%Y-%m-%d'))

    amount = forms.DecimalField(label="Сумма",
                                min_value=Decimal("0.01"),
                                max_value=Decimal("999999999.99"),
                                max_digits=11,
                                decimal_places=2)

    description = forms.CharField(label="Комментарий (необязательно)",
                                  required=False)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     fields_created_by_users = (("status", "статуса"),
    #                                ("subcategory", "подкатегории"))
    #
    #     for field_name, verbose_name in fields_created_by_users:
    #         value = cleaned_data.get(field_name)
    #         if value and getattr(value, "created_by", None) != self.user:
    #             self.add_error(field_name, f"Недопустимый выбор {verbose_name}")
    #
    #     return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.created_by = self.user
        if commit:
            instance.save()
        return instance
