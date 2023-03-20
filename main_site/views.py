from django.shortcuts import render
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from json import loads

from main_site.forms import FeedBackForm, SearchFromFileForm
from main_site.models import FeedbackContact, Suppliers, FileForSearch
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
    suppliers_inn_list = []

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

        # Добавляем ИНН в список, из таблицы будут удалены поставщики, которых нет в списке
        suppliers_inn_list.append(supplier.INN)
    
    Suppliers.objects.exclude(INN__in=suppliers_inn_list).delete()
    return JsonResponse({'status': "ok"})


import hashlib
from for_1C_tools import get_data
from bs4 import BeautifulSoup
import os

def search_suppliers(request: HttpRequest):
    contxt = {}
    if request.method == "GET":
        pass
    else:
        md5_hash = hashlib.md5()
        md5_hash.update(request.FILES["resorces_list"].read())
        
        file_for_search, new = FileForSearch.objects.get_or_create(
            hash_file=md5_hash.hexdigest()
        )

        if new:
            file_for_search.search_file = request.FILES["resorces_list"]
            file_for_search.save()

        path_for_1C = file_for_search.search_file.path.split("for_1C", 1)[1]
        path_for_1C = os.getenv("PREFFIX_SHARE_PATH", None) + path_for_1C
        path_for_1C = path_for_1C.replace("/", "\\")
        print(path_for_1C)
        params = {
            "File": path_for_1C,
            "HashMD5": md5_hash,
            "Range": "Found"
        }
        fake_params = {
            "File": r"\\SRV-1C-DEV\files_mcp_om\Вед. ресурсов 7 граф.xlsx",
            "HashMD5": md5_hash,
            "Range": "Found"
        }
        answer = get_data(
            "http://192.168.220.8/mcp_om/ws/stimdataexchange.1cws",
            "GetSuppliersResources",
            params
        )
        soap = BeautifulSoup(answer, features="lxml")
        status = soap.find("statuscode").get_text(strip=True)
        result = {}
        result["status"] = status
        
        if status == "200":
            
            result["res_total"] = soap.find("contractorresquantity").get_text(strip=True)
            result["sup_found"] = soap.find("suppliersquantity").get_text(strip=True)
            result["resources"] = []



            for resource in soap.find_all("resourcecontractor"):
                res = {}
                res["code_orig"] = resource.find("rescodeoriginal").get_text(strip=True)
                res["name"] = resource.find("resname").get_text(strip=True)
                # res["price_zone"] = resource.find("pricezone").get_text(strip=True)
                resource: BeautifulSoup
                print(resource.prettify())
                res["suppliers"] = []
                for supplier in resource.find_all("contragent"):
                    supp = {i.name: i.text for i in supplier.children if i.name}
                    res["suppliers"].append(supp)
                result["resources"].append(res)
            
        else:
            result["error_text"] = f"Произошла ошибка ({status})"
        
        contxt["result"] = result

    return render(request, 'search_suppliers.html', contxt)