from typing import Any, Callable
import requests

_api_url = "https://api.myanimelist.net/v2/"
_secondary_api_url = "https://myanimelist.net/v1/"

class _BasicReq:
    def __init__(self, headers: dict[str, str] | None = None):
        """
        Add params from API MAL GET and Headers from query
        """
        if(headers is None):
            self.headers = {}
            self.headers["Content-Type"] = "application/x-www-form-urlencoded"            
            self.headers["X-MAL-Client-ID"] = "6114d00ca681b7701d1e15fe11a4987e"
        else:
            self.headers = headers

    def _get(self, slug: str, params: dict | None = None) -> list[int,dict]:
        """Get request to https://api.myanimelist.net/v2/"""
        resp_get = requests.get(_api_url+slug,params=params,headers=self.headers)
        return [resp_get.status_code,resp_get.json()]
    
    def _post(self, slug: str, data: dict | None = None) -> list[int,dict]:
        """Post request to https://api.myanimelist.net/v2/"""
        resp_post = requests.post(_api_url+slug,headers=self.headers,data=data)
        return [resp_post.status_code,resp_post.json()]
    
    def _post_api_v1(self, slug:str, data: dict | None = None) -> list[int,dict]:
        """Post request to https://myanimelist.net/v1/, usally for get token account"""
        resp_post = requests.post(_secondary_api_url+slug,headers=self.headers,data=data)
        return [resp_post.status_code,resp_post.json()]
    
    def _patch(self, slug:str, data: dict | None = None) -> list[int,dict]:
        """Patch request to https://api.myanimelist.net/v2/"""
        resp_patch = requests.patch(_api_url+slug,headers=self.headers,data=data)
        return [resp_patch.status_code,resp_patch.json()]
    
    def _delete(self, slug:str, data: dict | None = None) -> list[int,dict]:
        """Delete request to https://api.myanimelist.net/v2/"""
        resp_del = requests.delete(_api_url+slug,headers=self.headers)
        return [resp_del.status_code,resp_del.json()]