import requests
import json
from django.conf import settings 

API_PATH = "/api/v1/"
API_HOST = "http://localhost"
API_PORT = "8000"

REQUEST_METHODS = {"PUT": requests.put,
                   "POST": requests.post,
                   "PATCH": requests.patch,
                   "DELETE": requests.delete,
                   "GET": requests.get}
HEADERS = {'content-type': 'application/json'}

def save(form, method=None):
    url = "{}:{}/{}/{}".format(settings.API_HOST,settings.API_PORT, settings.API_PATH, form.Meta.api_path)
    payload = form.to_dict()
    if method == None:
        if payload['id']:
            method = "PUT"
        else:
            method = "POST"
    if not REQUEST_METHODS[method]:
        raise Exception("Invalid reequest method: %s" % method)
    return REQUEST_METHODS[method](url, data=json.dumps(payload), headers=HEADERS)

def get(form, params=None):
    url = "{}:{}/{}/{}".format(settings.API_HOST,settings.API_PORT, settings.API_PATH, form.Meta.api_path)
    resp = requests.get(url, params)
    data = json.load(resp)
    return data