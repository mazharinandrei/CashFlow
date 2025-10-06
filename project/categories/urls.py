from django.urls import path

from . import views

app_name = "categories"

urlpatterns = [
    path("create/", views.CategoryCreateView.as_view(), name="create"),
    path("create/<int:type_pk>/", views.CategoryCreateView.as_view(), name="create-by-type-pk"),
    path("<int:pk>", views.CategoryDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", views.CategoryUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="delete"),
    path('get-options', views.get_categories_options_by_type, name="get-options-by-type"),

]
