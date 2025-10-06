from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from categories.models import Category
from main.mixins.base_delete_view import BaseDeleteViewMixin
from main.mixins.created_by_view import CreatedByViewMixin
from main.mixins.object_permission_required import ObjectPermissionRequiredMixin
from transaction_types.models import Type


class CategoryView:
    model = Category
    fields = ["name", "type"]
    template_name = "main/forms/basic_form.html"

    def get_success_url(self):
        return reverse_lazy("categories:detail", kwargs={'pk': self.object.pk})


class CategoryCreateView(LoginRequiredMixin, CreatedByViewMixin, CreateView):
    extra_context = {'title': "Добавление категории записей"}

    def get_initial(self):
        """
        Предзаполнение формы
        """
        initial = super().get_initial()
        type_pk = self.kwargs.get("type_pk")
        if type_pk:
            initial["type"] = type_pk  # предзаполняем поле type
        return initial


class CategoryDetailView(ObjectPermissionRequiredMixin, DetailView):
    model = Category


class CategoryUpdateView(CategoryView, ObjectPermissionRequiredMixin, CreatedByViewMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Редактирование категории «{self.object.name}»"
        return context


class CategoryDeleteView(CategoryView, BaseDeleteViewMixin):
    def get_success_url(self):
        return reverse_lazy("main:type", kwargs={'pk': self.object.type.pk})


def get_categories_options_by_type(request):
    context = {}
    pk = request.GET.get("type")
    try:
        pk = int(pk)
        type = Type.objects.get(pk=pk)
        context["options"] = type.categories.all()
    except:
        pass  # TODO: log
    return render(request, "main/components/select-options.html", context)
