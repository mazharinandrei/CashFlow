from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from main.mixins.base_delete_view import BaseDeleteViewMixin
from main.mixins.created_by_view import CreatedByViewMixin
from main.mixins.object_permission_required import ObjectPermissionRequiredMixin
from statuses.models import Status


class StatusView:
    model = Status
    fields = ["name"]
    template_name = "main/forms/basic_form.html"
    success_url = reverse_lazy("main:settings")


class StatusCreateView(StatusView, CreatedByViewMixin, LoginRequiredMixin, CreateView):
    extra_context = {'title': "Добавление статуса для записей"}


class StatusUpdateView(StatusView, ObjectPermissionRequiredMixin, UpdateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Редактирование статуса «{self.object.name}»"
        return context


class StatusDeleteView(BaseDeleteViewMixin, StatusView):
    success_url = reverse_lazy("main:settings")
