from bs4 import BeautifulSoup
from sys import argv

from for_1C_tools import get_data
import requests


with open("regions.txt") as f:

    regions = dict(i.strip().split(":") for i in f.readlines())


try:
    URL = argv[1]
except:
    URL = 'http://localhost:8000'
    print("Use default:", URL)

res = get_data(
    "http://192.168.220.8/mcp_om/ws/stimdataexchange.1cws",
    "GetRrp",
    {}
)

soap = BeautifulSoup(res, features="lxml")
# print(soap.prettify())
data = []

for contragent in soap.find_all("contragent"):
    supp = {i.name: i.text for i in contragent.children if i.name}
    supp["fromrrp"] = supp["fromrrp"] == "true"
    if supp["kpp"]:
        reg_code = supp["kpp"][:2]
    else:
        reg_code = supp["inn"][:2]
    title = regions.get(reg_code, "")
    supp["region"] = {
        "code": int(reg_code),
        "title": title
    }
    data.append(
        supp
    )
    # print()
    # print(regions.get(reg_code, ""))
    # print(data[-1])

prepeared_data = {"data": data}
requests.post(URL + '/suppliers/api/sync_suppliers', json=prepeared_data)