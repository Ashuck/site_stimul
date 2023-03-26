from suppliers.views import get_suppliers, sync_suppliers, search_suppliers
from django.urls import path

urlpatterns = [
    path('', get_suppliers, name='suppliers'),
    path('search', search_suppliers, name='search_suppliers'),
    path('api/sync_suppliers', sync_suppliers, name='sync_suppliers'),
]