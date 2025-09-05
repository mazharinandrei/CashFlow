from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class ObjectPermissionRequiredMixin(LoginRequiredMixin):
    """
    Сравнивает object.created_by и request.user.
    PermissionDenied, eсли объект создан другим пользователем
    """
    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().created_by == request.user:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)