# IMPORT PACKAGES
from .authorization import basic_auth
import requests
import json
from urllib import parse

# Global API variables
api_endpoint = '/api/v1'
page_get = '/get'
page_list = '/list'
type_list = '/contenttypes/list'
page_create = '/create'
page_update = '/update'
page_archive = '/archive'
page_fileupload = '/fileupload'
page_delete = '/delete'


# List content types
def list_contenttypes(admin_url, api_key, app_id):
    auth = basic_auth(api_key, app_id)
    if admin_url[-1] == '/':
        admin_url = admin_url[0:-1]
    url = admin_url + api_endpoint + type_list
    headers = {'Authorization': auth}

    payload = requests.request('GET',
                               url,
                               headers=headers)

    try:
        payload.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    return payload


# List pages for a specified content type
def list_pages(admin_url, api_key, app_id, content_type, queries: dict = None):
    auth = basic_auth(api_key, app_id)
    if admin_url[-1] == '/':
        admin_url = admin_url[0:-1]
    url = admin_url + api_endpoint + '/' + content_type + page_list
    headers = {'Authorization': auth}
    if queries:
        for key in queries:
            if '?' not in url:
                url = url + '?' + key + '=' + parse.quote(queries[key], safe='')
            else:
                url = url + '&' + key + '=' + parse.quote(queries[key], safe='')

    payload = requests.request('GET',
                               url,
                               headers=headers)

    try:
        payload.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    return payload


# Get a page by ID
def get_page(admin_url, api_key, app_id, content_type, page_id, language=None):
    auth = basic_auth(api_key, app_id)
    url = admin_url + api_endpoint + '/' + content_type + page_get + '?id=' + parse.quote(page_id, safe='')
    headers = {'Authorization': auth}

    if language:
        url = url + '&language=' + language

    payload = requests.request('GET',
                               url,
                               headers=headers)

    try:
        payload.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)

    return payload


# Deprecated single function to get, post, or delete pages using the OC API.
def oc_api(url, api_key, app_id, method='GET', body=''):
    # Basic authentication
    auth = basic_auth(api_key, app_id)

    if method == 'GET':
        r = requests.get(url=url,
                         headers={'Accept': 'application/json',
                                  'Authorization': auth}
                         )
    elif method == 'POST':
        r = requests.post(url=url,
                          data=json.dumps(body),
                          headers={'Content-Type': 'application/json',
                                   'Accept': 'application/json',
                                   'Authorization': auth}
                          )
    else:
        r = requests.delete(url=url,
                            data=body,
                            headers={'Accept': 'application/json',
                                     'Authorization': auth})
    return r
