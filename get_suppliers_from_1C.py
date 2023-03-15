from bs4 import BeautifulSoup
from sys import argv
import requests


def get_fields(content):
    fields = []
    for element in content.find("valuetable").findChildren("column"):
        fields.append(element.find("name").text)
    return fields

def wrap_xml(content):
    soup = BeautifulSoup()
    envelope = soup.new_tag("soap:Envelope")
    
    envelope["xmlns:soap"] = "http://www.w3.org/2003/05/soap-envelope"
    envelope["xmlns:ws"] = "http://www.cstim.ru/SaaS/1.0/WS"
    
    header = soup.new_tag("soap:Header")
    body = soup.new_tag("soap:Body")
    body.append(content)
    envelope.append(header)
    envelope.append(body)
    soup.append(envelope)
    return soup


def get_xml_content(tag_name, data: dict):
    soup = BeautifulSoup()
    method = soup.new_tag(f"ws:{tag_name}")
    for key, value in data.items():
        param = soup.new_tag(f"ns:{key}")
        param.append(str(value))
        method.append(param)
    return method


def get_data(url, method_name, params):
    method = get_xml_content(method_name, params)
    xml =  str(wrap_xml(method))
    print(xml)
    xml = xml.encode()
    
    result = requests.post(url, data=xml, auth=("StimDataExchange", "Cntgfirf2"))
    result = result.text.replace('&lt;', '<')
    result = result.replace('&gt;', '>')
    return result

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
requests.post(URL + '/api/sync_suppliers', json=prepeared_data)