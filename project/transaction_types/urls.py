from django.urls import path

from . import views

app_name = 'types'

urlpatterns = [
    path('create', views.TypeCreateView.as_view(), name="create"),
    path('<int:pk>', views.TypeDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', views.TypeUpdateView.as_view(), name="edit"),
    path('<int:pk>/delete/', views.TypeDeleteView.as_view(), name='delete'),
]
