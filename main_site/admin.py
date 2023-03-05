from django.contrib import admin

# Register your models here.
from main_site.models import Contacts, Services, Suppliers

@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    pass

@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    pass