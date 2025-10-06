from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.timezone import now

# Create your models here.

class Status(models.Model):
    """
    Статус записи (транзакции). 
    Например: Бизнес, Личное, Налог...
    """
    
    name = models.CharField(verbose_name="Наименование", 
                            max_length=100)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False 
    ) # https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model  
    # TODO: попробовать создать CreatedByMixin (например, https://habr.com/ru/articles/130566/)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Type(models.Model):
    """
    Тип записи (транзакции). 
    Например: Пополнение, Списание
    """
    name = models.CharField(verbose_name="Наименование", 
                            max_length=100)
    
class BaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )  
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

class Category(models.Model):
    """
    Категория записи (транзакции), привязанная к определённому типу. 
    Например: Инфраструктура, Маркетинг (Тип: Списание)
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )  

    name = models.CharField(verbose_name="Наименование", 
                            max_length=100)
    
    type = models.ForeignKey(verbose_name="Тип",
                            to=Type, 
                            on_delete=models.CASCADE,
                            related_name="categories")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Subcategory(models.Model):
    """
    Подкатегория записи (транзакции), привязанная к определённой категории.
    Например, для категории Маркетинг: Farpost, Avito
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False
    )  

    name = models.CharField(verbose_name="Наименование", 
                            max_length=100)
    
    category = models.ForeignKey(verbose_name="Категория",
                                 to=Category, 
                                 on_delete=models.CASCADE,
                                 related_name="subcategories")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Transaction(models.Model): 
    """
    Запись (транзакция) пользователя. 
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        editable=False # Помимо того, что editable запрещает изменять это поле, оно не позволяет его отображать в форме. окак
    ) # https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#referencing-the-user-model

    created_at = models.DateField(verbose_name="Дата записи", 
                                  default=now) # Пример записи — 01.01.2025
    
    status = models.ForeignKey(verbose_name="Статус",
                               to=Status, 
                               on_delete=models.CASCADE)
    
    subcategory = models.ForeignKey(verbose_name="Подкатегория",
                                    to=Subcategory,
                                    on_delete=models.CASCADE)  # Категорию вытащим из Субкатегории, Тип из Категории
    
    amount = models.DecimalField(verbose_name="Сумма",
                                 max_digits=11, 
                                 decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))]) # больше нуля
    
    description = models.CharField(verbose_name="Комментарий",
                                   max_length=200,
                                   blank=True, 
                                   null=True) # Необязательное поле
    def __str__(self):
        return f"{self.created_at}: {self.status}, {self.subcategory} — {self.amount} ({self.description})"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Запись"
        verbose_name_plural = "Записи"