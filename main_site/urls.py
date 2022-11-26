from django.urls import path
from main_site.views import get_main_page, get_services_page, get_contact_page

urlpatterns = [
    path('services', get_services_page),
    path('contacts', get_contact_page),
    path('', get_main_page),
]
