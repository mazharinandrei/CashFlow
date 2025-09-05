from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


app_name = 'main'  
  
urlpatterns = [  
    path('', views.index, name="index"),
    
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),

    path('settings', views.settings, name="settings"), # TODO: кажется, название не сильно подходит

    path('transaction/create', views.TransactionCreateView.as_view(), name="create-transaction"),
    path("transaction/<int:pk>/update", views.TransactionUpdateView.as_view(), name="edit-transaction"),
    path("transaction/<int:pk>/delete", views.TransactionDeleteView.as_view(), name="delete-transaction"),

    path('create-status', views.StatusCreateView.as_view(), name="create-status"),
    path('status/<int:pk>/update/', views.StatusUpdateView.as_view(), name="edit-status"),
    path('status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='delete-status'),


    path('type/create', views.TypeCreateView.as_view(), name="create-type"),
    path('type/<int:pk>', views.TypeDetailView.as_view(), name="type"),
    path('type/<int:pk>/update/', views.TypeUpdateView.as_view(), name="edit-type"),
    path('type/<int:pk>/delete/', views.TypeDeleteView.as_view(), name='delete-type'),

    path('category/create/', views.CategoryCreateView.as_view(), name="create-category"),
    path("category/create/<int:type_pk>/", views.CategoryCreateView.as_view(), name="create-category-by-type-pk"),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name="category"),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name="edit-category"),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete-category'),


    path('category/<int:category_pk>/create-subcategory/', views.SubcategoryCreateView.as_view(), name="create-subcategory"),
    path('subcategory/<int:pk>/update/', views.SubcategoryUpdateView.as_view(), name="edit-subcategory"),
    path('subcategory/<int:pk>/delete/', views.SubcategoryDeleteView.as_view(), name='delete-subcategory'),


    path('categories/get-options', views.get_categories_options_by_type, name="get-categories-options-by-type"),
    path('subcategories/get-options', views.get_subcategories_options_by_category, name="get-subcategories-options-by-category"),
]