from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from json import loads

from main_site.forms import FeedBackForm
from main_site.models import FeedbackContact, Suppliers
from main_site.email_working import send_mail
from main_site.models import Services, Contacts

# Create your views here.
def get_main_page(request):
    partners = [
        "/static/pic/partners/логотип цнэ.png",
        "/static/pic/partners/логотип цп.png",
        "/static/pic/partners/Логотип_ НИЦ ЭКСПЕРТИЗА_полиграфия.png",
        "/static/pic/partners/РОП логотип.png",
        "/static/pic/partners/СРО ИОС_логотип.png",
    ]
    contxt = {
        "partners": partners
    }
    return render(request, 'about.html', contxt)


def get_services_page(request):
    contxt = {}
    services = Services.objects.filter(visible=True)
    contxt["services"] = services
    return render(request, 'services.html', context=contxt)


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
            "Заявка от {fio}\nОрганизация: {firm_name}\nКонтакты: {phone}, {email}".format(**form.cleaned_data)
        )
    else:
        response_data["status"] = "error"
        response_data["msg"] = form.errors.as_text()
    return JsonResponse(response_data)


def get_suppliers(request):
    contxt = {"suppliers_list":Suppliers.objects.all()}
    return render(request, 'suppliers.html', contxt)


@csrf_exempt
@require_http_methods(["POST"])
def sync_suppliers(request):
    data = loads(request.body)
    suppliers_list = []
    for supplier_data in data["data"]:
        supplier, _ = Suppliers.objects.get_or_create(INN=supplier_data["inn"])
        supplier.title = supplier_data["name"]
        supplier.full_title = supplier_data["namefull"]
        supplier.OGRN = supplier_data["ogrn"]
        supplier.KPP = supplier_data["kpp"]
        supplier.address = supplier_data["addresslegal"]
        supplier.post_address = supplier_data["addresspostal"]
        supplier.type = supplier_data["type"]
        supplier.email = supplier_data["email"]
        supplier.phone = supplier_data["phone"]
        supplier.save()
        suppliers_list.append(supplier)
    Suppliers.objects.exclude(INN__in=[s.INN for s in suppliers_list]).delete()
    return JsonResponse({'status': "ok"})

"""{'name': 'АО "УНИВЕРСАМ № 3"', 
'namefull': 'АКЦИОНЕРНОЕ ОБЩЕСТВО "УНИВЕРСАМ № 3"', 
'inn': '4401109228', 
'kpp': '440101001', 
'ogrn': '1104401004630', 
'addresslegal': '156019, КОСТРОМСКАЯ ОБЛАСТЬ, Г. КОСТРОМА, УЛ. ИНДУСТРИАЛЬНАЯ, Д. 55, НЕЖИЛОЕ ПОМЕЩЕНИЕ 132 КОМНАТА 3', 
'addresspostal': '', 
'type': '', 
'email': '', 
'phone': '+7 (4942) 49-12-00, +7 (4942) 49-12-22, +7 (4942) 49-12-45'}"""