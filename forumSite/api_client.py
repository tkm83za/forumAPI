import requests
import logging
import json
#from django.conf import settings 
settings = {}
API_PATH = settings.get('API_PATH', "/api/v1")
API_HOST = settings.get('API_HOST', "http://localhost")
API_PORT = settings.get('API_PORT', "8000")

REQUEST_METHODS = {"PUT": requests.put,
                   "POST": requests.post,
                   "PATCH": requests.patch,
                   "DELETE": requests.delete,
                   "GET": requests.get}
HEADERS = {'content-type': 'application/json'}

logger = logging.getLogger(__name__)

def save(form, method=None):
    url = "{}:{}{}/{}".format(API_HOST, API_PORT, API_PATH, form.Meta.api_path)
    payload = form.to_dict()
    if method == None:
        if payload.get('id', False):
            method = "PUT"
        else:
            method = "POST"
    if not REQUEST_METHODS[method]:
        raise Exception("Invalid reequest method: %s" % method)
    logger.debug("%s: %s" % (method, url))
    return REQUEST_METHODS[method](url, data=json.dumps(payload), headers=HEADERS)

def get(form, params=None):
    url = "{}:{}{}/{}".format(API_HOST, API_PORT, API_PATH, form.Meta.api_path)
    logger.debu("GET: %s" % url)
    resp = requests.get(url, params)
    data = json.load(resp)
    return data