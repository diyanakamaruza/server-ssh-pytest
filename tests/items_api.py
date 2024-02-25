import requests
from urllib.parse import urlencode

 
environment = {
    'local': 'http://127.0.0.1:5000',                  # DEV # 
    'docker': 'http://host.docker.internal:5000',      # STG # Local docker
    'public': 'https://items-api.diyana.kamaruza.com', # PRD # Status page -> https://diyana.kamaruza.com/status
    }


class ItemsApi:

    def __init__(self, hostname=environment['local'], endpoint='items'):
        self.url = f'{hostname}/{endpoint}/'

    def __request(self, method, url, json=None, timeout=120):
        try: 
            if method == 'GET':
                return requests.get(url, timeout=timeout)
            elif method == 'POST':
                return requests.post(url, json=json, timeout=timeout)
            elif method == 'DELETE':
                return requests.delete(url, timeout=timeout)
            else:
                assert False, '(!) Expecting request method "GET" or "POST" or "DELETE"!'
        except requests.exceptions.HTTPError as e: 
            assert False, f'(!) HTTP error: {e.args[0]}'
        except requests.exceptions.ReadTimeout as e: 
            assert False, f'(!) Timeout error: {e.args[0]}'
        except requests.exceptions.ConnectionError as e: 
            assert False, f'(!) Connection error: {e.args[0]}'
        except requests.exceptions.RequestException as e: 
            assert False, f'(!) Request exception error: {e.args[0]}'

    def get(self, url):
        return self.__request('GET', url)

    def post(self, url, data):
        return self.__request('POST', url, data)

    def delete(self, url):
        return self.__request('DELETE', url)

    def get_items(self):
        return self.get(self.url)

    def get_items_count(self):
        return len(self.get_items().json())

    def get_items_by_name(self, name):
        if type(name) is not str:
            assert False, '(!) Expecting input type "str" for parameter "name". Example: "item_2".'
        return self.get(self.url + name)

    def get_items_by_param(self, param):
        if type(param) is not dict:
            assert False, '(!) Expecting input type "dict" for parameter "param". Example: {"name": "item_2"}.'
        return self.get(self.url + '?' + urlencode(param))

    def add_item(self, item):
        if type(item) is not dict:
            assert False, '(!) Expecting input type "dict" for parameter "item". Example: {"name": "item_2", "email": "item_2@ssh.com"}.'
        return self.post(self.url, item)

    def delete_item(self, name):
        if type(name) is not str:
            assert False, '(!) Expecting input type "str" for parameter "name". Example: "item_2".'       
        return self.delete(self.url + name)
