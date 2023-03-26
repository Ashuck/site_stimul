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


class Services(models.Model):
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
    
    choices = (
        (0, "Без ссылки"),
        (1, "На страницу"),
        (2, "На описание")
    )

    title = models.CharField("Название", max_length=1320)
    visible = models.BooleanField("Видимость", default=True)
    url_type = models.IntegerField("Тип ссылки", choices=choices, default=0)
    url_page = models.URLField("Страница", default=None, null=True, blank=True)
    detail = models.TextField("Описание", default="", blank=True)
    
    def __str__(self):
        return self.title
    
    def get_paragraphs(self):
        for p in self.detail.split("\n"):
            yield p


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


class Managers(models.Model):
    class Meta:
        verbose_name = "Руководитель"
        verbose_name_plural = "Руководство"
        ordering = ("order_index",)
    
    FIO = models.CharField("ФИО", max_length=300)
    about = models.TextField("Биография")
    Photo = models.ImageField("Фото", upload_to="pictures/managers")
    JobFunction = models.CharField("Должность", max_length=36) 
    order_index = models.IntegerField("Очередность сортировки", default=0)

    def __str__(self) -> str:
        return f"{self.JobFunction}: {self.FIO}"

    def get_paragraphs(self):
        for p in self.about.split("\n"):
            yield p


class Partners(models.Model):
    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ("order_index",)

    title = models.CharField("Имя компании", max_length=50)
    site_url = models.URLField("Сайт партнера")
    logo = models.ImageField("Лого", upload_to="pictures/pertners_logo")
    order_index = models.IntegerField("Очередность сортировки", default=0)

    def __str__(self) -> str:
        return self.title


class Sliders(models.Model):
    class Meta:
        verbose_name = "Кадр слайдера"
        verbose_name_plural = "Кадры сладера"
        ordering = ("order_index",)
    
    title = models.CharField("Имя слайда", max_length=60)
    image = models.ImageField("Картинка слайдера", upload_to="pictures/slader_frames")
    order_index = models.IntegerField("Очередность сортировки", default=0)
    slider_tag = models.CharField("Уникальный тэг слайдера", max_length=6)

    def __str__(self) -> str:
        return f"{self.title} для {self.slider_tag}"
