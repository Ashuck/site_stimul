from django.db import models

# Create your models here.
class FeedbackContact(models.Model):
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты для обратной связи"
    
    email = models.EmailField("Електронная почта")
    phone = models.TextField("Номер телефона")
    firm_name = models.TextField("Название организации")
    fio = models.TextField("ФИО контакта")

    def __str__(self) -> str:
        return self.firm_name


class Suppliers(models.Model):
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
    
    INN = models.CharField("ИНН", max_length=32)
    title = models.CharField("Название", max_length=320)
    email = models.EmailField("Електронная почта")
    address = models.CharField("Адрес", max_length=1320)
    phone = models.TextField("Номер телефона")
    site_url = models.URLField("Сайт", max_length=320)
    price = models.FileField("Прайс-лист")
    
    def __str__(self) -> str:
        return f"{self.title} ({self.INN})"


class Supplier_products(models.Model):
    class Meta:
        verbose_name = "Товар поставщика"
        verbose_name_plural = "Товары поставщиков"
    
    title = models.CharField("Название", max_length=320)
    supplier = models.ForeignKey(Suppliers, models.CASCADE, related_name="products")

    def __str__(self) -> str:
        return self.title