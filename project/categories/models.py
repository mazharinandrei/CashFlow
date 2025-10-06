from django.db import models

from main.models import BaseModel
from transaction_types.models import Type


class Category(BaseModel):
    """
    Категория записи (транзакции), привязанная к определённому типу.
    Например: Инфраструктура, Маркетинг (Тип: Списание)
    """

    name = models.CharField(
        verbose_name="Наименование",
        max_length=100
    )

    type = models.ForeignKey(
        verbose_name="Тип",
        to=Type,
        on_delete=models.CASCADE,
        related_name="categories"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "categories"