from django.shortcuts import render
from suppliers.models import Suppliers, FileForSearch, Regions
from json import loads
from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q


def get_suppliers(request: HttpRequest):
    part_name = request.GET.get("search", "")
    from_rrp = request.GET.get("from_rrp")
    region_codes = list(map(int, request.GET.getlist("region")))
    supplier_list = Suppliers.objects.all()

    if part_name:
        supplier_list = supplier_list.filter(
            Q(title__contains=part_name) |
            Q(full_title__contains=part_name) |
            Q(INN__contains=part_name) |
            Q(OGRN__contains=part_name)
        )
    if from_rrp:
        supplier_list = supplier_list.filter(fromrrp=True)
    if region_codes:
        supplier_list = supplier_list.filter(region__in=region_codes)
    
    contxt = {
        "suppliers_list": supplier_list,
        "regions": Regions.objects.all(),
        "selected_regions": region_codes,
        "from_rrp": from_rrp,
        "search": part_name
    }
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
        supplier.fromrrp = supplier_data["fromrrp"]
        region, _ = Regions.objects.get_or_create(
            reg_code=supplier_data["region"]["code"],
            title=supplier_data["region"]["title"]
        )
        supplier.region = region
        supplier.save()

        # Добавляем ИНН в список, из таблицы будут удалены поставщики, которых нет в списке
        suppliers_inn_list.append(supplier.INN)
    
    Suppliers.objects.exclude(INN__in=suppliers_inn_list).delete()
    return JsonResponse({'status': "ok"})
# Create your views here.
import hashlib
from for_1C_tools import get_data
from bs4 import BeautifulSoup
import os

def search_suppliers(request: HttpRequest):
    contxt = {}
    if request.method == "GET":
        pass
    else:
        print(request.POST)
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
            "HashMD5": md5_hash.hexdigest(),
            "Range": request.POST.get("search_renge", "Found"),
            "Period": request.POST.get("period", "All")
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
        result["file_name"] = str(request.FILES["resorces_list"])
        if status == "200":
            
            result["res_total"] = soap.find("contractorresquantity").get_text(strip=True)
            result["sup_found"] = soap.find("suppliersquantity").get_text(strip=True)
            result["resources"] = []

            for resource in soap.find_all("resourcecontractor"):
                res = {}
                res["code_orig"] = resource.find("rescodeoriginal").get_text(strip=True)
                res["name"] = resource.find("resname").get_text(strip=True)
                res["suppliers"] = []
                for supplier in resource.find_all("contragent"):
                    supp = {i.name: i.text for i in supplier.children if i.name}
                    supp["price_zone"] = resource.find("pricezone").get_text(strip=True)
                    res["suppliers"].append(supp)
                result["resources"].append(res)
            
        else:
            result["error_text"] = f"Произошла ошибка ({status})"
        
        contxt["result"] = result

    return render(request, 'search_suppliers.html', contxt)