from django.db import models

from categories.models import Category
from main.models import BaseModel


class Subcategory(BaseModel):
    """
    Подкатегория записи (транзакции), привязанная к определённой категории.
    Например, для категории Маркетинг: Farpost, Avito
    """

    name = models.CharField(
        verbose_name="Наименование",
        max_length=100)

    category = models.ForeignKey(
        verbose_name="Категория",
        to=Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        db_table = "subcategories"
