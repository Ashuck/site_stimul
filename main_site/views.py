from django.shortcuts import render

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