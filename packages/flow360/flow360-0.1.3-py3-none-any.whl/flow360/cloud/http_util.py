"""
http utils. Example:
http.get(path)
"""
from functools import wraps

import requests

from flow360 import Env, __version__
from flow360.cloud.security import api_key
from flow360.component.utils import is_valid_uuid


def api_key_auth(request):
    """
    Set the authentication.
    :param request:
    :return:
    """
    key = api_key()
    if not key:
        raise ValueError("API key not found, please set it by commandline: flow360 configure.")
    request.headers["simcloud-api-key"] = key
    request.headers["flow360-python-version"] = __version__
    return request


def http_interceptor(func):
    """
    Intercept the response and raise an exception if the status code is not 200.
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """A wrapper function"""

        # Extend some capabilities of func
        resp = func(*args, **kwargs)
        if resp.status_code == 401:
            raise Exception("Unauthorized.")

        if resp.status_code == 404:
            return None

        if resp.status_code == 200:
            result = resp.json()
            return result.get("data")

        raise Exception(f"Unexpected response: {resp.status_code}")

    return wrapper


class Http:
    """
    Http util class.
    """

    def __init__(self, session: requests.Session):
        self.session = session

    @http_interceptor
    def get(self, path: str, json=None):
        """
        Get the resource.
        :param path:
        :param json:
        :return:
        """
        return self.session.get(url=Env.current.get_real_url(path), auth=api_key_auth, json=json)

    @http_interceptor
    def post(self, path: str, json=None):
        """
        Create the resource.
        :param path:
        :param json:
        :return:
        """
        return self.session.post(Env.current.get_real_url(path), json=json, auth=api_key_auth)

    @http_interceptor
    def put(self, path: str, json):
        """
        Update the resource.
        :param path:
        :param json:
        :return:
        """
        return self.session.put(Env.current.get_real_url(path), data=json, auth=api_key_auth)

    @http_interceptor
    def delete(self, path: str):
        """
        Delete the resource.
        :param path:
        :return:
        """
        return self.session.delete(Env.current.get_real_url(path), auth=api_key_auth)


http = Http(requests.Session())


class RestApi:
    def __init__(self, endpoint, id=None):
        is_valid_uuid(id, ignore_none=True)
        self._id = id
        self._endpoint = endpoint
        self._info = None

    def _url(self, method):
        url = f'{self._endpoint}'
        if self._id is not None:
            url += f'/{self._id}'
        if method is not None:
            url += f'/{method}'
        return url


    def init_id(self, id):
        if self._id is None:
            self._id = id
        else:
            raise RuntimeError('"id" already set, change of "id" is not allowed.')        

    def get(self, path=None, method=None, json=None):
        return http.get(path or self._url(method), json=json)

    def post(self, json, path=None, method=None):            
        return http.post(path or self._url(method), json=json)

    def put(self, json, path=None, method=None):            
        return http.put(path or self._url(method), json=json)

    def delete(self, path=None, method=None):            
        return http.put(path or self._url(method))
