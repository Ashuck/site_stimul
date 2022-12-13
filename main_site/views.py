from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from main_site.forms import FeedBackForm
from main_site.models import FeedbackContact
from main_site.email_working import send_mail


# Create your views here.
def get_main_page(request):
    return render(request, 'about.html')


def get_services_page(request):
    services = """Разработка сметной документации
        Информационная поддержка процесса и порядка определения сметной стоимости
        Корректировка сметной документации
        Финасовый аудит
        Бухгалтерский учет
        Строительство жилых и нежилых зданий
        Строительство автомобильных дорог и автомагистралей
        Строительство инженерных коммуникаций для водоснабжения и водоотведения, газоснабжения
        Строительство коммунальных объектов для обеспечения электроэнергией и телекоммуникациями"""
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