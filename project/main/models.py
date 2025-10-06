from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )

    created_at = models.DateField(
        verbose_name="Дата создания",
        auto_now_add=True,
        editable=False)

    updated_at = models.DateField(
        verbose_name="Дата обновления",
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True

    def __str__(self):
        if self.name:
            return self.name
        else:
            return f"{self._meta.verbose_name} #{self.id}"


