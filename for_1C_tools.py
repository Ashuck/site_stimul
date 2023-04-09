from bs4 import BeautifulSoup
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


def set_attrs(param, attrs):
    for attr_key, attr_val in attrs.items():
        param[attr_key] = attr_val
    return param

def get_xml_content(tag_name, data: dict, preffix="ws:", attributes=None) -> BeautifulSoup:
    # создаем корневой тэг
    soup = BeautifulSoup()
    method = soup.new_tag(preffix + tag_name)
    
    if attributes:
        method = set_attrs(method, attributes)
    # перебираем параметры внутри тэга
    for key, value in data.items():
        if isinstance(value, dict):
            # аттрибуты задаются только параметрам корневого тэга
            # то есть аттрибуты для корневого тэга необходимо задать вне функции
            attrs = value.get("attributies", {})

            # имена тэга можно вложить, сделано специально для возможности повторения имен на одном уровне
            # В качесве ключа необходимо использовать уникальное значение
            tag_name = value.get("tag_name", key)
            if isinstance(value["value"], dict):

                # Если внутри параметра не текстовое значение, а структура из тэгов, то рекурсивно добавляем их
                param = get_xml_content(tag_name, value["value"], preffix)
            else:
                param = soup.new_tag(preffix + tag_name)
            method.append(set_attrs(param, attrs))            

        else:
            # Для простых случаев, когда параметр состоит только из тэга и текстового значения
            param = soup.new_tag(preffix + key)
            param.append(str(value))
            method.append(param)
    return method

from base64 import b64encode, b64decode
def get_data(url, method_name, params, preffix="ws:", attributes=None):
    method = get_xml_content(method_name, params, preffix, attributes)
    # m = b64encode(str(method).encode()).decode()

    xml =  wrap_xml(method)
    # xml =  wrap_xml(m)
    print(xml.prettify())
    xml = str(xml).encode()
    # xml = b64encode(xml)
    result = requests.post(url, data=xml, auth=("StimDataExchange", "Cntgfirf2"))
    result = result.text.replace('&lt;', '<')
    result = result.replace('&gt;', '>')
    return result


if __name__ == "__main__":
    params = {
        "param1": "123",
        "param2": {
            "attributies": {
                "attr1": 1,
                "attr2": "432"
            },
            "value": "dsa"
        },
        "param3": {
            "value": {
                "asd": "rewr",
                "ewe": ""
            }
        },
        1: {
            "tag_name": "param1",
            "value": {
                "asd": "rewr",
                "ewe": "",
                "param3": {
                    "value": {
                        "asd": "rewr",
                    }
                },
            }
        },
        2: {
            "tag_name": "param1",
            "attributies": {
                "attr1": 123,
                "attr2": 123
            },
            "value": {
                "asd": "rewr",
                "ewe": "",
                "param3": {
                    "value": {
                        "asd": "rewr",
                    }
                },
            }
        },
    }
    result = get_xml_content("Test", params)
    print(result.prettify())