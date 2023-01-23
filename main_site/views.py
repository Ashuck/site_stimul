from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from main_site.forms import FeedBackForm
from main_site.models import FeedbackContact, Suppliers
from main_site.email_working import send_mail


# Create your views here.
def get_main_page(request):
    return render(request, 'about.html')


def get_services_page(request):
    services = """Разработка сметной документации
        Расчет заработной платы рабочего 1 разряда, занятого в строительстве
        Мониторинг цен строительных ресурсов, машин, оборудования и механизмов
        Разработка конъюнктурного анализа цен для объектов капитального строительства
        Консультации прохождения экспертизы проектной документации и результатов инженерных изысканий
        Продажа/техническое сопровождение/ консультирование по программному обеспечению в сфере ценообразования в строительстве
        Пересчет сметной стоимости по постановлению Правительства РФ № 1315
        Контроль качества строительных материалов (Знак качества)
        Реестр рекомендованных поставщиков"""
    contxt = {
        "services": services.split("\n")
    }
    return render(request, 'services.html', context=contxt)


def get_contact_page(request):
    contxt = {
        "contacts": [
            {
                "name": "ИНН/ОГРН:",
                "value": "3702256016 / 1213700003098"
            },
            {
                "name": "Адрес регистрации:",
                "value": "Ивановская обл, г.о. Иваново, г Иваново, ул Крутицкая, д. 20А, помещ. 11"
            },
            {
                "name": "Телефон:",
                "value": "+7(4932)773576"
            },
            {
                "name": "email:",
                "value": "stimul37Iv@yandex.ru"
            },

        ]
    }
    return render(request, 'contacts.html', context=contxt)


@require_http_methods(["POST"])
def take_contacts(request):
    form = FeedBackForm(request.POST)
    response_data = {}
    if form.is_valid():
        response_data["status"] = "ok"
        response_data["msg"] = "Заявка принята. С Вами в скором времени свяжутся"
        # form.save()
        
        send_mail(
            "Заявка от {fio}\nОрганизация: {firm_name}\nКонтакты: {phone}, {email}".format(**form.cleaned_data)
        )
    else:
        response_data["status"] = "error"
        response_data["msg"] = form.errors.as_text()
    return JsonResponse(response_data)


def get_suppliers(request):
    return render(request, 'suppliers.html')