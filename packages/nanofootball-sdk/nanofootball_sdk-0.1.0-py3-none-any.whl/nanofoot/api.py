import requests
import yaml
from pathlib import Path
from requests.sessions import Session

import logging

logger=logging.getLogger('nanofoot.api')

class LoginFailedException(Exception):
    pass

class CsrfTokenNotFound(Exception):
    pass

class Urls:
    def __init__(self,server='http://nanofootball.com'):
        self._server=server
    @property
    def home(self):
        return self._server
    @property
    def login(self):
        return self._server+'/login/'
    @property
    def video(self):
        return self._server+'/video/api/all/'
    def video_by_id(self,id):
        return self.video+str(id)+'/' #you need to ad a slash at the end or goddamit patch command wont work
    @property
    def exercises(self):
        return self._server+'/exercises/exercises_api'
    @property
    def exercises_web_page(self):
        return self._server+'/exercises/'
    @property
    def api_exercises(self):
        return self._server+'/api/exercises'

def credentials_from_file(path):
    with open(path,'r') as f:
        credentials=yaml.safe_load(f)
    return credentials.get('username'),credentials.get('password'),credentials.get('token')

def find_credentials(path) -> Path:
    """ returns the real path for credentials file
    it searches local dir, then the home dir"""
    file_in_home_dir=Path.home() / Path(path)
    file_in_current_dir=Path(path)
    if file_in_current_dir.exists() and file_in_home_dir.is_file():
        return file_in_current_dir
    elif file_in_home_dir.exists() and file_in_home_dir.is_file():
        return file_in_home_dir
    else:
        return None
    
    

class Api:
    def __init__(self, username=None,password=None, token=None,from_file='nanofootball-credentials.yaml'):
        if not username or not password or not token:
            credentials_file=find_credentials(path=from_file)
            if credentials_file is not None:
                username,password,token=credentials_from_file(path=credentials_file)
            else:
                raise AttributeError('Credentials not set. Credentials file not found.')
        self.urls=Urls()
        self.session=Session()
        self.token=token

        self.session.get(url=self.urls.login) # to get csrf token
        #csrf=self.session.cookies['csrftoken']

        auth_payload={
            'username': username,
            'password':password,
            'csrfmiddlewaretoken':self.csrf_token
        }
        resp=self.session.post(url=self.urls.login,data=auth_payload)

        if not resp.ok or 'class="error"' in resp.text:
            raise LoginFailedException(f'Cant login to {self.urls.home}. Check your usernamne and login')
    @property
    def csrf_token(self):
        csrf=self.session.cookies.get('csrftoken',None)
        if csrf:
            return csrf
        else:
            raise CsrfTokenNotFound('Cant fing CSRF Token. Maybe login flow failed.')
    @property
    def headers(self):
         return {
            'X-CSRFToken':self.csrf_token,
            'X-Requested-With': 'XMLHttpRequest' ### именно в этом апи такой заголовок важен для /exercises/exercises_api
        }
    def request(self,*args,**kwargs):
        """returns a request done with request lib
        args and kwargs same as request.resquest(...)
        
        if headers=None - do csrf headers from self.headers"""
        if not kwargs.get('headers'):
            kwargs['headers']=self.headers
            
        return self.session.request(*args,**kwargs)

