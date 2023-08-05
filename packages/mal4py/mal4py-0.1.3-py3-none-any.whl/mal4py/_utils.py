import json
import secrets
from mal4py._basic import _BasicReq, _secondary_api_url
from mal4py._query import MalAnime, MalManga, MalForum, MalUser

def get_new_code_verifier() -> str:
    """Generate new Code Verifier from Auth"""
    token = secrets.token_urlsafe(100)
    return token[:128]

class _MalToken():
    """Class for Generate Token for Session on API MAL"""
    def __init__(self, token_type: str,access_token: str,refresh_token: str,expires_in: int | None):
        self.token_type: str = token_type
        self.expires_in: int | None = expires_in
        self.access_token: str = access_token
        self.refresh_token: str = refresh_token
    
    def __str__(self):
        return f'{self.__dict__}'

    def _from_json_obj(obj: dict["token_type": str,"access_token": str,"refresh_token": str, "expires_in": int | None]): 
        """Get MalToken From Token JSON Object"""
        try:
            return _MalToken(
                obj["token_type"],
                obj["access_token"],
                obj["refresh_token"],
                obj["expires_in"]
            )
        except:
            raise Exception("Error: dict verify struct")

    def _from_json_string(string: str):
        """Get MalToken From Token JSON String"""
        obj: dict[
            "token_type": str,
            "access_token": str,
            "refresh_token": str,
            "expires_in": int | None,
        ] = json.loads(string)
        try:
            return _MalToken(
                obj["token_type"],
                obj["access_token"],
                obj["refresh_token"],
                obj["expires_in"]
            )
        except:
            raise Exception("Error: json_string verify struct")

    async def _from_credential(client_id: str,username: str,password: str):
        """
        **Unstable!** Get MalToken From Login And Password
        """
        DATA = {
            "client_id": client_id,
            "grant_type": "password",
            "username": username,
            "password": password
        }
        REQ = _BasicReq()
        res = REQ._post("auth/token",data=DATA)
        if(res[0]==200):
            return _MalToken(
                res[1]["token_type"],
                res[1]["access_token"],
                res[1]["refresh_token"],
                res[1]["expires_in"]
            )
        else:
            res[1].update({"status": res[0]})
            raise Exception(res[1])

    async def _from_refresh_token(client_id: str, client_secret: str, refresh_token: str):
        """Get MalToken From Refresh Token"""
        DATA = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
        REQ = REQ = _BasicReq()
        res = REQ._post_api_v1("oauth2/token",data=DATA)
        if(res[0]==200):
            return _MalToken(
                res[1]["token_type"],
                res[1]["access_token"],
                res[1]["refresh_token"],
                res[1]["expires_in"]
            )
        else:
            res[1].update({"status": res[0]})
            raise Exception(res[1])

    async def _from_authorization_code(client_id: str,client_secret: str,code: str,code_verifier: str): 
        """
        Get _MalToken From PKCE Authorization Code
        """
        DATA = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": code_verifier,
        }
        REQ = REQ = _BasicReq()
        res = REQ._post_api_v1("oauth2/token",data=DATA)
        if(res[0]==200):
            return _MalToken(
                res[1]["token_type"],
                res[1]["access_token"],
                res[1]["refresh_token"],
                res[1]["expires_in"]
            )
        else:
            res[1].update({"status": res[0]})
            raise Exception(res[1])

class _MalAccount():
    """Class for create session some login methods"""
    def __init__(self, client_id: str, client_secret: str, mal_token: _MalToken | None = None):
        self.__client_id: str = client_id
        self.__client_secret: str = client_secret
        self.__mal_token: _MalToken = mal_token
        self.anime:MalAnime = MalAnime(self.__get_http_headers())
        self.manga: MalManga = MalManga(self.__get_http_headers())
        self.forum: MalForum = MalForum(self.__get_http_headers())
        self.user: MalUser = MalUser(self.__get_http_headers())
        
    @property
    def client_id(self) -> str:
        return self.__client_secret
    @property
    def client_secret(self) -> str:
        return self.__client_secret
    @property
    def mal_token(self) -> _MalToken:
        return self.__mal_token
    
    @client_id.setter
    def client_id(self, id):
        self.__client_id = id
    @client_secret.setter
    def client_secret(self, secret):
        self.__client_secret = secret
    @mal_token.setter
    def mal_token(self, mal_token: _MalToken):
        self.__mal_token = mal_token

    def stringify_token(self) -> str:
        """Get MalToken data as string"""
        if not(self.__mal_token is None):
            return json.dumps(self.__mal_token.__dict__)
        else:
            return None
    
    async def refresh_token(self):
        """Authorize with refresh Token"""
        if not(self.__mal_token is None):
            self.__mal_token = await _MalToken._from_refresh_token(
                self.__client_id,
                self.__client_secret,
                self.__mal_token
            )
        return self

    def __get_http_headers(self):
        """Header session for Request to MAL API"""
        HEADERS: dict[str, str] = {
            #'Content-Type': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            "Authorization": None,
            "X-MAL-CLIENT-ID": self.__client_id
        }
        if not(self.__mal_token is None):
            HEADERS["Authorization"] = "Bearer %s" %(self.__mal_token.access_token)
        return HEADERS

class Auth():
    """Use initialized api (Auth) to login
        you must have this data:
        - client_id: your Client ID
        - client_secret: if your application has a Client Secret; OMIT in all other cases (i.e. you selected "Android", "iOS", or "Other" as App Type)
        - code: the user's Authorization Code after call get_oauth_url
        - code_verifier: the Code Verifier generated with function get_new_code_verifier()
    """
    def __init__(self,client_id: str = "6114d00ca681b7701d1e15fe11a4987e",client_secret: str = ""):
        self.__client_id = client_id
        self.__client_secret = client_secret

    def load_token(self, token: _MalToken):
        """Load MalToken saved from 'stringifyToken()'"""
        return _MalAccount(self.__client_id, self.__client_secret, token)

    def get_oauth_url(self,code_challenge: str) -> str:
        """Get OAuth url for code challenge or code verifier can use get_new_code_verifier function"""
        return  "%soauth2/authorize?response_type=code&client_id=%s&code_challenge=%s&state=RequestID42" %(_secondary_api_url,self.__client_id,code_challenge)

    async def authorize_with_refreshtoken(self,refresh_token: str) -> _MalAccount: 
        """If more time has passed you can also refresh token instead of loading last one"""
        MALTOKEN = await _MalToken._from_refresh_token(self.__client_id,self.__client_secret,refresh_token)
        return _MalAccount(self.__client_id,self.__client_secret,MALTOKEN)

    async def authorize_with_code(self, code: str,code_challenge: str) -> _MalAccount:
        """
        Open returned url, accept oauth and use returned code to authorize
        It is actually a `code_verifier` but mal accepts code_challenge here instead
        """
        MALTOKEN = await _MalToken._from_authorization_code(self.__client_id,self.__client_secret,code,code_challenge)
        return _MalAccount(self.__client_id, self.__client_secret, MALTOKEN)

    def authorize_with_json_obj(self, json_obj: dict["token_type": str,"access_token": str,"refresh_token": str, "expires_in": int | None]) -> _MalAccount:
        """Get MalToken From Token JSON Dict"""
        MALTOKEN = _MalToken._from_json_obj(json_obj)
        return _MalAccount(self.__client_id, self.__client_secret, MALTOKEN)
    
    def authorize_with_json_string(self, json_str: str) -> _MalAccount:
        """Get MalToken From Token JSON String"""
        MALTOKEN = _MalToken._from_json_string(json_str)
        return _MalAccount(self.__client_id,self.__client_secret, MALTOKEN)
    
    async def unstable_login(self,username: str, password: str) -> _MalAccount:
        """### Login to API using login and password `(Unstable!)`"""
        MALTOKEN = await _MalToken._from_credential(self.__client_id,username,password)
        return _MalAccount(self.__client_id,self.__client_secret, MALTOKEN)
    
    async def guest_login(self) -> _MalAccount:
        """### You can use some API functions, BEWARE `(Unstable!)`"""
        return _MalAccount(self.__client_id,self.__client_secret, None)