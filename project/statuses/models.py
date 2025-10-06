from django.db import models

from main.models import BaseModel


class Status(BaseModel):
    """
    Статус записи (транзакции).
    Например: Бизнес, Личное, Налог...
    """

    name = models.CharField(
        verbose_name="Наименование",
        max_length=100
    )

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"
        db_table = "statuses"
