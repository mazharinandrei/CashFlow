from django.urls import path

from . import views

app_name = "subcategories"

urlpatterns = [
    path('<int:pk>/update/', views.SubcategoryUpdateView.as_view(), name="edit"),
    path('<int:pk>/delete/', views.SubcategoryDeleteView.as_view(), name='delete'),
    path('get-options', views.get_subcategories_options_by_category,
         name="get-options-by-category"),

    path('create/<int:category_pk>/', views.SubcategoryCreateView.as_view(),
         name="create"),
]
