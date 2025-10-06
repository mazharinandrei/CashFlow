from django.views.generic import DeleteView

from main.mixins.object_permission_required import ObjectPermissionRequiredMixin


class BaseDeleteViewMixin(ObjectPermissionRequiredMixin, DeleteView):
    """
    Base delete view for all models. Used to confirm delete. Object permission required.
    """
    template_name = 'main/forms/confirm_delete.html'
    success_url = None
