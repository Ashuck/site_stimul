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