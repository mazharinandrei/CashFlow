from django.urls import path
from django.contrib.auth.views import LogoutView

from transactions.views import TransactionListView
from . import views


app_name = 'main'  

urlpatterns = [
    path('', TransactionListView.as_view(), name="index"),
    path('signup', views.SignUp.as_view(), name="signup"),
    path('login', views.LoginUser.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('settings', views.settings, name="settings"),
]