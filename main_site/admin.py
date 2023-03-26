from django.contrib import admin

# Register your models here.
from main_site.models import Contacts, Services, Managers, Partners, Sliders

@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    pass

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    pass

@admin.register(Managers)
class ManagersAdmin(admin.ModelAdmin):
    pass

@admin.register(Partners)
class PartnersAdmin(admin.ModelAdmin):
    pass

@admin.register(Sliders)
class SlidersAdmin(admin.ModelAdmin):
    pass