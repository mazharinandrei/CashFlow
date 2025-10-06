from django.urls import path

from . import views

app_name = "transactions"

urlpatterns = [
    path("create", views.TransactionCreateView.as_view(), name="create"),
    path("<int:pk>/update", views.TransactionUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete", views.TransactionDeleteView.as_view(), name="delete"),
]
