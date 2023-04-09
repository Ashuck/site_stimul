from suppliers.views import get_suppliers, sync_suppliers, search_suppliers, send_resource_request
from django.urls import path

urlpatterns = [
    path('', get_suppliers, name='suppliers'),
    path('search', search_suppliers, name='search_suppliers'),
    path('api/sync_suppliers', sync_suppliers, name='sync_suppliers'),
    path('send_request', send_resource_request)
]