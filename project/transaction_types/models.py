from django.db import models

from main.models import BaseModel


class Type(BaseModel):
    """
    Тип записи (транзакции).
    Например: Пополнение, Списание
    """
    name = models.CharField(
        verbose_name="Наименование",
        max_length=100
    )

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"
        db_table = "transaction_types"
