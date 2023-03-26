from bs4 import BeautifulSoup
from sys import argv

from for_1C_tools import get_data
import requests


try:
    URL = argv[1]
except:
    URL = 'http://localhost:8080'
    print("Use default:", URL)

res = get_data(
    "http://192.168.220.8/mcp_om/ws/stimdataexchange.1cws",
    "GetRrp",
    {}
)

soap = BeautifulSoup(res, features="lxml")

data = []

for contragent in soap.find_all("contragent"):
    data.append(
        {i.name: i.text for i in contragent.children if i.name}
    )

prepeared_data = {"data": data}
requests.post(URL + '/suppliers/api/sync_suppliers', json=prepeared_data)