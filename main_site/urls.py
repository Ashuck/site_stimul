from django.urls import path
from main_site.views import (
    get_main_page, get_services_page, get_contact_page, 
    take_contacts, get_expirience, get_managers, get_service_detail
)

urlpatterns = [
    path('services', get_services_page, name='services'),
    path('services/detail', get_service_detail, name='service_detail'),
    path('contacts', get_contact_page, name='contacts'),
    path('feedback', take_contacts, name='feedback'),
    path('expirience', get_expirience, name='expirience'),
    path('managers', get_managers, name='managers'),
    path('', get_main_page, name='main'),
]
