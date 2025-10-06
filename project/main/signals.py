from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from subcategories.models import Subcategory
from .defaults import DEFAULT_USER_DATA
from categories.models import Category
from statuses.models import Status
from transaction_types.models import Type


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def on_user_register(sender, instance, created, **kwargs):
    """
    Действия при регистрации пользователя
    """
    if created:
        transaction.on_commit(lambda: _create_defaults_for_user(instance))


def _create_defaults_for_user(new_user):
    """
    Добавление дефолтных Статусов, Типов, Категорий и Подкатегорий для только что зарегистрированного пользователя
    """
    
    """
    пояснение для меня будущего и других читателей:

        здесь у нас ведутся три листа с объектами (new_type_objects, category_objects_to_bulk, subcategory_objects_to_bulk),
        которые в конце отправляются на bulk_create 

        листы ведутся для того, чтобы не дёргать из БД свежесозданные типы, категории и подкатегории во время итераций

        мы связываем в zip объекты класса Type (new_type_objects) с типами из словаря выше (DEFAULT_USER_DATA),

        пробегаемся по каждой категории, создаём instance категории, добавляем его в список category_objects_to_bulk,

        и расширяем список подкатегорий пачкой instanc'ов подкатегорий

        после этого уже отправляем всё на bulk_create (+ bulk_creat'ом создаём дефолтные статусы)
    """
    
    new_type_objects = [Type(name=new_type["type_name"], created_by=new_user) for new_type in DEFAULT_USER_DATA["types"]]
    
    category_objects_to_bulk = [] # 
    subcategory_objects_to_bulk = []

    for type_object, dict_type in zip(new_type_objects, DEFAULT_USER_DATA["types"]):
        
        for dict_category in dict_type["categories"]:

            category_object = Category(type=type_object,
                                                name=dict_category["category_name"], 
                                                created_by=new_user)
            
            category_objects_to_bulk.append(category_object)
            
            subcategory_objects_to_bulk.extend(Subcategory(category=category_object, 
                                                            name=new_subcategory_name, 
                                                            created_by=new_user) 
                                                            for new_subcategory_name in dict_category["subcategories"])


    Status.objects.bulk_create([Status(name=status_name, created_by=new_user) 
                                for status_name in DEFAULT_USER_DATA["statuses"]])  
    Type.objects.bulk_create(new_type_objects)
    Category.objects.bulk_create(category_objects_to_bulk)
    Subcategory.objects.bulk_create(subcategory_objects_to_bulk)

