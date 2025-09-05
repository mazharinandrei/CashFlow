from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.core.paginator import Paginator

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .forms import TransactionsFilterForm, TransactionModelForm

from .models import Category, Status, Subcategory, Transaction, Type

from .mixins import ObjectPermissionRequiredMixin

def view_403(request, exception=None): #TODO: обрабатывать, логировать
    return redirect("/")

def view_404(request, exception=None): #TODO: обрабатывать, логировать
    return redirect("/")

class SignUp(CreateView):
    form_class = UserCreationForm
    template_name = "main/forms/signup_form.html"
    extra_context = {'title': "Регистрация", "button_text": "Создать аккаунт"}
    
    def get_success_url(self):
        return reverse_lazy('main:index')

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "main/forms/login_form.html"
    extra_context = {'title': "Вход", "button_text": "Войти"}
    
    def get_success_url(self):
        return reverse_lazy('main:index')

@login_required
def index(request):
    # передаём в контекст параметры, чтобы давать ссылку на страницы с фильтрами
    _request_copy = request.GET.copy()
    parameters = _request_copy.pop('page', True) and _request_copy.urlencode()

    # используется в шаблоне для отображения / скрытия кнопки "Сбросить" 
    has_filters = any(
        field in parameters for field in ("subcategory", "category", "type", "status", "date_from", "date_to")
    ) 

    transactions = Transaction.objects.filter(created_by=request.user).order_by("-created_at", "-pk")
    
    form = TransactionsFilterForm(user=request.user, data=request.GET)
    
    if form.is_valid():
        
        """
        записи подкатегории < записи категории < записи типа
        сначала фильтруем по самому ограничивающему данному параметру
        """

        if form.cleaned_data.get("subcategory"):
            transactions = transactions.filter(subcategory=form.cleaned_data.get("subcategory"))
        
        elif form.cleaned_data.get("category"):
            category = Category.objects.get(pk=form.cleaned_data.get("category").pk)
            transactions = transactions.filter(subcategory__in=category.subcategories.all())
        
        elif form.cleaned_data.get("type"):
            categories_of_type = Category.objects.filter(type= form.cleaned_data.get("type"))
            subcategories = Subcategory.objects.filter(category__in=categories_of_type)
            transactions = transactions.filter(subcategory__in = subcategories)
            
    
        # фильтрация по остальным параметрам, не связанным между собой

        if form.cleaned_data.get("status"):
            transactions = transactions.filter(status=form.cleaned_data.get("status"))
        
        if form.cleaned_data.get("date_from"):
           transactions = transactions.filter(created_at__gte=form.cleaned_data.get("date_from"))

        if form.cleaned_data["date_to"]:
            transactions = transactions.filter(created_at__lte=form.cleaned_data["date_to"])


    paginator = Paginator(transactions, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    num_page = paginator.num_pages


    context = {
        "page_obj": page_obj,
        "paginator": paginator,
        "page_number": page_number,
        "num_page":num_page,
        "parameters": parameters,


        "title":"Главная страница",
        "statuses": Status.objects.filter(created_by=request.user),
        "types": Type.objects.filter(created_by=request.user),
        
        "form": form,

        "has_filters": has_filters,
        "index": True, # чтобы не отображать ссылку на главную
    }
    return render(request, 'main/index.html', context)

@login_required
def settings(request):
    statuses = Status.objects.filter(created_by=request.user)
    types = Type.objects.filter(created_by=request.user)
    context = {
        "title":"Управление справочниками",
        "statuses":statuses,
        "types": types,
    } 
    return render(request, 'main/settings.html', context)


"""
CREATE VIEWS
"""


class TypeCreateView(LoginRequiredMixin, CreateView):
    model = Type
    fields = ["name"]  
    template_name = "main/forms/basic_form.html"
    extra_context = {'title': "Добавление типа записей"}

    def form_valid(self, form):
        # назначаем автора перед сохранением
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("main:type", kwargs={'pk': self.object.pk})
        

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ["name"]  
    template_name = "main/forms/basic_form.html"
    success_url = reverse_lazy("main:settings")
    extra_context = {'title': "Добавление статуса для записей"}
    
    def form_valid(self, form):
        # назначаем автора перед сохранением
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name", "type"]  
    template_name = "main/forms/basic_form.html"
    extra_context = {'title': "Добавление категории записей"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["type"].queryset = Type.objects.filter(created_by=self.request.user) # фильтрация по текущему пользователю
        return form

    def get_initial(self):
        """
        Предзаполнение формы
        """
        initial = super().get_initial()
        type_pk = self.kwargs.get("type_pk")
        if type_pk:
            initial["type"] = type_pk  # предзаполняем поле type
        return initial

    def form_valid(self, form):
        # дополнительная защита от подмены данных
        if form.cleaned_data["type"].created_by != self.request.user:
            form.add_error("type", "Недопустимый выбор типа")
            return self.form_invalid(form)
    
        form.instance.created_by = self.request.user # назначаем автора перед сохранением
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("main:category", kwargs={'pk': self.object.pk})


class SubcategoryCreateView(LoginRequiredMixin, CreateView):
    model = Subcategory
    fields = ["name", "category"]
    template_name = "main/forms/basic_form.html"
    extra_context = {'title': "Добавление подкатегории записей"}

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["category"].queryset = Category.objects.filter(created_by=self.request.user) # фильтрация по текущему пользователю
        return form

    def get_initial(self):
        initial = super().get_initial()
        category_pk = self.kwargs.get("category_pk")
        if category_pk:
            initial["category"] = category_pk  # предзаполняем поле type
        return initial

    def form_valid(self, form):
        # дополнительная защита от подмены данных
        if form.cleaned_data["category"].created_by != self.request.user:
            form.add_error("category", "Недопустимый выбор категории")
            return self.form_invalid(form)
        # назначаем автора перед сохранением
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy("main:category", kwargs={'pk': self.object.category.pk})


class TransactionCreateView(CreateView):
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


"""
DETAIL VIEWS
"""


class TypeDetailView(ObjectPermissionRequiredMixin, DetailView):
    model = Type

class CategoryDetailView(ObjectPermissionRequiredMixin, DetailView):
    model = Category


"""
UPDATE VIEWS
"""


class TypeUpdateView(ObjectPermissionRequiredMixin, UpdateView):
    model = Type
    template_name = 'main/forms/basic_form.html'
    fields = ['name']
    success_url = reverse_lazy("main:settings")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['title'] = f"Редактирование типа «{self.object.name}»"
        return context 


class CategoryUpdateView(ObjectPermissionRequiredMixin, UpdateView):
    model = Category
    template_name = 'main/forms/basic_form.html'
    fields = ["name", "type"]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["type"].queryset = Type.objects.filter(created_by=self.request.user) # фильтрация по текущему пользователю
        return form

    def form_valid(self, form):
        # дополнительная защита от подмены данных
        if form.cleaned_data["type"].created_by != self.request.user:
            form.add_error("type", "Недопустимый выбор типа")
            return self.form_invalid(form)
        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("main:type", kwargs={'pk': self.object.type.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['title'] = f"Редактирование категории «{self.object.name}»"
        return context 


class SubcategoryUpdateView(ObjectPermissionRequiredMixin, UpdateView):
    model = Subcategory
    template_name = 'main/forms/basic_form.html'
    fields = ['name', "category"]
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["category"].queryset = Category.objects.filter(created_by=self.request.user) # фильтрация по текущему пользователю
        return form

    def form_valid(self, form):
        # дополнительная защита от подмены данных
        if form.cleaned_data["category"].created_by != self.request.user:
            form.add_error("category", "Недопустимый выбор категории")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("main:category", kwargs={'pk': self.object.category.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['title'] = f"Редактирование подкатегории «{self.object.name}»"
        return context 


class StatusUpdateView(ObjectPermissionRequiredMixin, UpdateView):
    model = Status
    template_name = 'main/forms/basic_form.html'
    fields = ['name']
    success_url = reverse_lazy("main:settings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['title'] = f"Редактирование статуса «{self.object.name}»"
        return context 


class TransactionUpdateView(ObjectPermissionRequiredMixin, UpdateView):
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


"""
DELETE VIEWS
"""


class StatusDeleteView(ObjectPermissionRequiredMixin, DeleteView):
    model = Status
    template_name = 'main/forms/confirm_delete.html'
    success_url = reverse_lazy("main:settings")

class TypeDeleteView(ObjectPermissionRequiredMixin, DeleteView):
    model = Type
    template_name = 'main/forms/confirm_delete.html'
    success_url = reverse_lazy("main:settings")

class CategoryDeleteView(ObjectPermissionRequiredMixin, DeleteView):
    model = Category
    template_name = 'main/forms/confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy("main:type", kwargs={'pk': self.object.type.pk})

class SubcategoryDeleteView(ObjectPermissionRequiredMixin, DeleteView):
    model = Subcategory
    template_name = 'main/forms/confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy("main:category", kwargs={'pk': self.object.category.pk})

class TransactionDeleteView(ObjectPermissionRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'main/forms/confirm_delete.html'
    success_url = reverse_lazy("main:index")


"""
FBV ДЛЯ HTMX
"""


def get_categories_options_by_type(request):
    context = {}
    pk = request.GET.get("type")
    try:
        pk = int(pk)
        type = Type.objects.get(pk=pk)
        context["options"] = type.categories.all()
    except:
        pass
    return render(request, "main/components/select-options.html", context)

def get_subcategories_options_by_category(request):
    context = {}
    pk = request.GET.get("category")
    try:
        pk = int(pk)
        category = Category.objects.get(pk=pk)
        context["options"] = category.subcategories.all()
    except:
        pass
    return render(request, "main/components/select-options.html", context)