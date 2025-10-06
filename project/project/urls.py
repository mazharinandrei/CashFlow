from django.contrib import admin
from django.urls import include, path

handler403 = 'main.views.view_403'
handler404 = 'main.views.view_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace="main")),
    path('statuses/', include('statuses.urls', namespace="statuses")),
    path('categories/', include('categories.urls', namespace="categories")),
    path('subcategories/', include('subcategories.urls', namespace="subcategories")),
    path('transactions/', include('transactions.urls', namespace="transactions")),
    path('transaction_types/', include('transaction_types.urls', namespace="types")),
]
