from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from main_site.forms import FeedBackForm
from main_site.models import FeedbackContact
from main_site.email_working import send_mail
from main_site.models import Services, Contacts, Managers, Partners, Sliders

# Create your views here.
def get_main_page(request):
    contxt = {
        "partners": Partners.objects.all(),
        "slides": Sliders.objects.filter(slider_tag="m1")
    }
    return render(request, 'about.html', contxt)


def get_services_page(request):
    contxt = {}
    services = Services.objects.filter(visible=True)
    contxt["services"] = services
    return render(request, 'services.html', context=contxt)

def get_service_detail(request):
    contxt = {
        "service": Services.objects.get(id=request.GET.get('service_id', 1))
    }
    return render(request, 'service_detail.html', context=contxt)

def get_contact_page(request):
    contxt = {
        "contacts": Contacts.objects.all()
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
            "Заявка от {fio}\nОрганизация: {firm_name}\nКонтакты: {phone}, {email}".format(**form.cleaned_data),
            'Обратная связь КОС'
        )
    else:
        response_data["status"] = "error"
        response_data["msg"] = form.errors.as_text()
    return JsonResponse(response_data)


def get_expirience(request):
    return render(request, 'expirience.html')


def get_managers(request):
    contxt = {
        "managers": Managers.objects.all()
    }
    return render(request, "managers.html", context=contxt)