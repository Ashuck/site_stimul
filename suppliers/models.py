from django.db import models


class Regions(models.Model):
    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"
        ordering=("title",)
    
    reg_code = models.IntegerField("Код региона", primary_key=True)
    title = models.CharField("Название", max_length=32, unique=True)

    def __str__(self) -> str:
        return self.title


class Suppliers(models.Model):
    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"
        ordering=("-fromrrp",)
    
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
    fromrrp = models.BooleanField("Из реестра рекомендованных поставщиков", default=True)
    region = models.ForeignKey(Regions, models.PROTECT, verbose_name="Регион регистрации", null=True)
    
    def __str__(self) -> str:
        return f"{self.title} ({self.INN})"

# Create your models here.
class FileForSearch(models.Model):
    class Meta:
        verbose_name = "Файл для поиска"
        verbose_name_plural = "Файлы для поиска"
    
    search_file = models.FileField("Файл", upload_to="for_1C/from_site/%Y/%m/%d/")
    hash_file = models.TextField("Хэшсумма")

    def __str__(self):
        return str(self.id)