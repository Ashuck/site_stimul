from django.urls import path
from main_site.views import (
    get_main_page, get_services_page, get_contact_page, 
    take_contacts, get_suppliers
)

urlpatterns = [
    path('services', get_services_page, name='services'),
    path('contacts', get_contact_page, name='contacts'),
    path('feedback', take_contacts, name='feedback'),
    path('suppliers', get_suppliers, name='suppliers'),
    path('', get_main_page, name='main'),
]
