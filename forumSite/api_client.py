import requests
import logging
import json
from django.conf import settings 
#settings = {}

DEFAULTS = {'API_PATH': "/api/v1",
            'API_HOST': "http://localhost",
            'API_PORT': "80"}
if not settings.configured:
    settings.configure(DEFAULTS, DEBUG=False)
    
API_PATH = settings.API_PATH
API_HOST = settings.API_HOST
API_PORT = settings.API_PORT

REQUEST_METHODS = {"PUT": requests.put,
                   "POST": requests.post,
                   "PATCH": requests.patch,
                   "DELETE": requests.delete,
                   "GET": requests.get}
HEADERS = {'content-type': 'application/json'}

logger = logging.getLogger("forumSite.forms")

def save(form, method=None, request=None, payload=None):
    url = "{}:{}{}/{}".format(API_HOST, API_PORT, API_PATH, form.Meta.api_path)
    if form.initial.get('id', None) is not None:
        url = "{}:{}{}/{}{}/".format(API_HOST, API_PORT, API_PATH, form.Meta.api_path, form.initial['id'])
    if not payload:
        payload = form.to_dict(request=request)

    if method == None:
        if payload.get('id', False):
            method = "PUT"
        else:
            method = "POST"
    logger.error("%s: %s, %s" % (method, url, json.dumps(payload)))
    if not REQUEST_METHODS[method]:
        logger.debug("Exception raised!")
        raise Exception("Invalid request method: %s" % method)

    logger.debug("%s: %s" % (method, url))
    return REQUEST_METHODS[method](url, data=json.dumps(payload), headers=HEADERS)

def get(form, sub_url=None):
    if not sub_url:
        url = "{}:{}{}/{}".format(API_HOST, API_PORT, API_PATH, form.Meta.api_path)
        if form.initial.get('id', None) is not None:
            url = "{}:{}{}/{}{}/".format(API_HOST, API_PORT, API_PATH, form.Meta.api_path, form.initial['id'])
    else:
        url = "{}:{}{}/{}".format(API_HOST, API_PORT, API_PATH, sub_url)
    logger.debug("GET: %s" % url)
    resp = requests.get(url)
    data = resp.json()
    return data