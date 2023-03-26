from django.contrib import admin
from suppliers.models import Suppliers, FileForSearch
# Register your models here.

@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    pass

@admin.register(FileForSearch)
class FileForSearchAdmin(admin.ModelAdmin):
    pass