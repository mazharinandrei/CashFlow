from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from categories.models import Category
from main.mixins.base_delete_view import BaseDeleteViewMixin
from main.mixins.created_by_view import CreatedByViewMixin
from main.mixins.object_permission_required import ObjectPermissionRequiredMixin
from subcategories.models import Subcategory


class SubcategoryView:
    model = Subcategory
    fields = ["name", "category"]
    template_name = "main/forms/basic_form.html"

    def get_success_url(self):
        return reverse_lazy("categories:detail", kwargs={'pk': self.object.category.pk})


class SubcategoryCreateView(SubcategoryView, LoginRequiredMixin, CreatedByViewMixin, CreateView):
    extra_context = {'title': "Добавление подкатегории записей"}

    def get_initial(self):
        initial = super().get_initial()
        category_pk = self.kwargs.get("category_pk")
        if category_pk:
            initial["category"] = category_pk
        return initial


class SubcategoryUpdateView(SubcategoryView, ObjectPermissionRequiredMixin, CreatedByViewMixin, UpdateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Редактирование подкатегории «{self.object.name}»"
        return context


class SubcategoryDeleteView(SubcategoryView, BaseDeleteViewMixin):
    ...


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
