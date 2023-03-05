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
    KPP = models.CharField("КПП", max_length=32)
    OGRN = models.CharField("ОГРН", max_length=32)
    title = models.CharField("Название", max_length=320)
    full_title = models.CharField("Полное название", max_length=1320, default="")
    email = models.EmailField("Електронная почта")
    address = models.CharField("Адрес фактический", max_length=1320)
    post_address = models.CharField("Адрес почтовый", max_length=1320)
    type = models.CharField("Тип", max_length=32)
    phone = models.TextField("Номер телефона")
    site_url = models.URLField("Сайт", max_length=320)
    price = models.FileField("Прайс-лист", null=True, blank=True)
    
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


class Services(models.Model):
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    title = models.CharField("Название", max_length=1320)
    visible = models.BooleanField("Видимость", default=True)
    
    def __str__(self):
        return self.title


class Contacts(models.Model):
    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
        ordering = ("order_index",)
    
    name = models.CharField("Название", max_length=1320)
    value = models.CharField("Значение", max_length=1320)
    visible = models.BooleanField("Видимость", default=True)
    order_index = models.IntegerField("Приоритет", default=0)

    def __str__(self):
        return f"{self.order_index} {self.name}: {self.value}"