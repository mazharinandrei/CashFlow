from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from main.models import BaseModel
from statuses.models import Status
from subcategories.models import Subcategory


class Transaction(BaseModel):
    """
    Запись (транзакция) пользователя.
    """

    status = models.ForeignKey(
        verbose_name="Статус",
        to=Status,
        on_delete=models.CASCADE
    )

    # Категорию вытащим из Субкатегории, Тип из Категории
    subcategory = models.ForeignKey(
        verbose_name="Подкатегория",
        to=Subcategory,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        verbose_name="Сумма",
        max_digits=11,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]  # больше нуля
    )

    description = models.CharField(
        verbose_name="Комментарий",
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.created_at}: {self.status}, {self.subcategory} — {self.amount} ({self.description})"

    class Meta:
        ordering = ["-created_at", "-pk"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        db_table = "transactions"
