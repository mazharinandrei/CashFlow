from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, ListView

from main.mixins.base_delete_view import BaseDeleteViewMixin
from main.mixins.created_by_view import CreatedByViewMixin
from main.mixins.object_permission_required import ObjectPermissionRequiredMixin
from subcategories.models import Subcategory
from transactions.forms import TransactionModelForm, TransactionsFilterForm
from transactions.models import Transaction


class TransactionView:
    model = Transaction
    form_class = TransactionModelForm
    template_name = 'main/forms/basic_form.html'
    success_url = reverse_lazy("main:index")

    def get_form_kwargs(self):
        """
        Передаём в форму request.user
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'main/index.html'
    paginate_by = 8

    def get_queryset(self):
        self.form = TransactionsFilterForm(user=self.request.user, data=self.request.GET)
        qs = Transaction.objects.filter(created_by=self.request.user)

        if self.form.is_valid():
            cd = self.form.cleaned_data

            """
            записи подкатегории < записи категории < записи типа
            сначала фильтруем по самому ограничивающему данному параметру
            """

            if cd.get("subcategory"):
                qs = qs.filter(subcategory=cd["subcategory"])
            elif cd.get("category"):
                qs = qs.filter(subcategory__in=cd["category"].subcategories.all())
            elif cd.get("type"):
                qs = qs.filter(subcategory__in=Subcategory.objects.filter(category__type=cd["type"]))

            # остальные фильтры
            if cd.get("status"):
                qs = qs.filter(status=cd["status"])
            if cd.get("date_from"):
                qs = qs.filter(created_at__gte=cd["date_from"])
            if cd.get("date_to"):
                qs = qs.filter(created_at__lte=cd["date_to"])

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # GET-параметры без page для ссылок на фильтры
        parameters = self.request.GET.copy()
        parameters.pop('page', None)
        parameters_encoded = parameters.urlencode()

        context.update({
            "form": self.form,
            "has_filters": bool(parameters),
            "parameters": parameters_encoded,
            "title": "Главная страница",
            "index": True,
        })

        return context


class TransactionCreateView(TransactionView, CreatedByViewMixin, CreateView):
    ...


class TransactionUpdateView(TransactionView, CreatedByViewMixin, ObjectPermissionRequiredMixin, UpdateView):
    ...


class TransactionDeleteView(BaseDeleteViewMixin, TransactionView):
    success_url = reverse_lazy("main:index")
