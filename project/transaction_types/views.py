from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from main.mixins.base_delete_view import BaseDeleteViewMixin
from main.mixins.created_by_view import CreatedByViewMixin
from main.mixins.object_permission_required import ObjectPermissionRequiredMixin
from transaction_types.models import Type


class TypeView:
    model = Type
    fields = ["name"]
    template_name = "main/forms/basic_form.html"

    def get_success_url(self):
        return reverse_lazy("types:detail", kwargs={'pk': self.object.pk})


class TypeCreateView(TypeView, CreatedByViewMixin, LoginRequiredMixin, CreateView):
    extra_context = {'title': "Добавление типа записей"}


class TypeDetailView(ObjectPermissionRequiredMixin, DetailView):
    model = Type


class TypeUpdateView(TypeView, ObjectPermissionRequiredMixin, UpdateView):
    success_url = reverse_lazy("main:settings")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Редактирование типа «{self.object.name}»"
        return context


class TypeDeleteView(BaseDeleteViewMixin):
    model = Type
    success_url = reverse_lazy("main:settings")
