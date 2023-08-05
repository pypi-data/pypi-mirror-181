class SourceFileNotFound(Exception):
    pass

class VideoUploadError(Exception):
    pass

class VideoDeleteError(Exception):
    pass

class VideoGetError(Exception):
    pass

from .api import Api
import pathlib
import logging
from tqdm import tqdm
from typing import Callable,Iterable

logger=logging.getLogger('nanofoot.video')

class Folder:
    def __init__(self,data):
        self._data=data
    @property
    def name(self):
        return self._data['name']
    @property
    def location(self):
        return self._data['short_name']

def take_first(object):
    return next(iter(object))


class Exercise:
    def __init__(self,data):
        self._data=data    
        self._folder=None
    @property
    def name(self):

        return take_first(self._data['title'].values())
    @property
    def id(self):
        return self._data.get('id')
    @property
    def folder(self) -> Folder:
        if self._folder:
            return self._folder
        else:
            self._folder=Folder(data=self._data['folder'])
            return self._folder
    def __str__(self):
        return f'[{self.folder.location}] {self.name}'

class Video:
    def __init__(self,data):
        self._data=data
        self._exercises=None
    @property
    def raw_data(self):
        return self._data
    @property
    def id(self):
        return self._data['id']
    @property
    def _exercises_count(self):
        return len(self._data['exercises'])
    @property
    def exercises(self)->list[Exercise]:
        if self._exercises_count!=1:
            logger.info(f'Video {self.id} has {self._exercises_count} folders')
        if self._exercises:
            return self._exercises
        else:
            self._exercises=[Exercise(data=exs_data) for exs_data in self._data['exercises']]
            return self._exercises
    @property
    def name(self):
        return self._data['name']
    def __str__(self):
        return f'{self.name}'+f'\n    {self.url}'+f'\n    @ {self.source_name}'+ ''.join(f'\n    {exercise}' for exercise in self.exercises)
    @property
    def source_id(self):
        return self._data['videosource_id']['id']
    @property
    def source_name(self):
        return self._data['videosource_id']['name']
    @property
    def nftv_id(self):
        return self._data['links']['nftv']
    @property
    def youtube_id(self):
        return self._data['links']['youtube']
    @property
    def duration(self):
        return self._data['duration']
    @property
    def url(self):
        return f'http://nanofootball.com/video/?id={self.id}'
    @property
    def has_exercises(self):
        return True if self.exercises else False 

    def is_in_folder_with(self,**kwargs):
        """
        returns true is this wideo lives in folder with params=kwargs
        video.is_in_folder(location='B3')"""
        return any([all([getattr(exercise.folder,param)==kwargs[param] for param in kwargs]) for exercise in self.exercises])



class IterFilter:
    def __init__(self,basic_iter,func):
        self.func=func
        self.basic_iter=basic_iter # the one we get items and filter them
    def __next__(self):
        for item in self.basic_iter:
            # if item.id==6524:
            #     print('yo')
            if self.func(item):
                return item
        raise StopIteration
    def __iter__(self):
        return self

class ApiIter:
    def __init__(self, url, headers,session,return_class):
        self._session=session
        self._headers=headers
        self._next=url
        self.return_class=return_class

        self.buffer=[]
        self._i=None
        self._total=None

        self._current=None
      
    def where(self,func:Callable[[Video],bool]):
        """
        returns new iter with filtering by func paramenter
        """
        return iter(IterFilter(basic_iter=self,func=func))
    def with_bar(self,position=None, desc=None,leave=True):
        iterator=iter(self) # so this we init all needed values like total
        return tqdm(iterator,total=self._total,position=position,desc=desc,leave=leave)

    def first(self):
        self.populate_buffer()
    def __iter__(self):
        self.first()
        return self
    def __next__(self):
        received=self.populate_buffer()
        if received:
            return self.return_class(data=self.buffer.pop())
        else:
            raise StopIteration
    def __len__(self):
        return self._total

    def _request(self):
        resp=self._session.get(self._next)
        if resp.ok:
            return resp.json()
        else:
            raise Exception("Server side error")
    def populate_buffer(self):
        if len(self.buffer)>0:
            return True
        else:
            if self._next: # if we have some on selver
                data=self._request()
                self._total=data['count']
                self._next =data['next']
                self.buffer.extend(data['results'])
                return True
            else:
                return False # No more vids

class NotUpdatable:
    pass

def is_updatable(obj):
    return not isinstance(obj,NotUpdatable)


class VideoService:
    def __init__(self, api:Api=None):
        if not api:
            api=Api()
        self._api:Api=api

    def get(self, id):
        url=self._api.urls.video_by_id(id)
        resp=self._api.session.get(url=url,headers=self._headers)


        if not resp.ok:
            if resp.status_code==404: #Not found
                return None
            else:
                with open('error.html','w',encoding='utf8') as f:
                    f.write(resp.text)
                    #logger.error('dumped to error.html')
                raise VideoGetError(f'error getting {id}. More info in error.html')

        if resp.status_code==200: #No content
            pass
        else:
            logger.warn(f'Some stuff with delete. expected 204 statuc code but got {resp.status_code}')
        return Video(data=resp.json())

    def delete(self, id:str):
        url=self._api.urls.video_by_id(id)
        resp=self._api.session.delete(url=url,headers=self._headers)
        if not resp.ok:
            with open('error.html','w',encoding='utf8') as f:
                f.write(resp.text)
                #logger.error('dumped to error.html')
            raise VideoDeleteError(f'error deleting {id}. more info in error.html')

        if resp.status_code==204: #No content
            pass
        else:
            logger.warn(f'Some stuff with delete. expected 204 statuc code but got {resp.status_code}')
        return True


    @property
    def _headers(self):
        return {
                'X-CSRFToken':self._api.csrf_token
            }

    def upload(self,
            path:str,
            title:str,
            video_source:int=1,#default=NF
            youtube_link='')-> Video:

        #checks
        file=pathlib.Path(path)
        if not file.exists() and file.is_file():
            raise SourceFileNotFound(f'Cant find file {path}. Wrong route or is folder')
        filename=file.name
        #network stuff
        with open(path,'rb') as video_handler:
            files={
                'file_video':  (filename,video_handler,'video/mp4'),
                'file_screen': b'',
                }

            payload={
                'name': title,
                'youtube_link':youtube_link,
                'second_screensaver': '',
                'videosource_id':  video_source,
                'duration': '',
                'language': 'none',
                'taggit': '[]',
            }

            headers=self._headers

            resp=self._api.session.post(
                url=self._api.urls.video,
                files=files,
                data=payload,
                headers=headers)

            
            if not resp.ok:
                with open('error.html','w',encoding='utf8') as f:
                    f.write(resp.text)
                    #logger.error('dumped to error.html')
                raise VideoUploadError(f'error uploading {path}. more info in error.html')

            if resp.status_code==201: #CREATED
                pass
            else:
                logger.warn(f'some stuff with upload must be status code 201 but its {resp.status_code}')
            return Video(data=resp.json())

    def patch(self,video_id,file_video:str=NotUpdatable(),file_screen=NotUpdatable(),**kwargs):
        if 'id' in kwargs:
            raise Exception('Update method doest receive id. We cant change video id')

        files={}
        if is_updatable(file_video):
            file=pathlib.Path(file_video)
            if not file.exists() and file.is_file():
                raise SourceFileNotFound(f'Cant find file {file_video}. Wrong route or is folder')
            filename=file.name
            video_handler=open(file_video,'rb')
            files['file_video']=(filename,video_handler,'video/mp4')
        if is_updatable(file_screen):
            raise NotImplemented('cant update screensavet atm')
        
        url=self._api.urls.video_by_id(video_id)
        payload=kwargs| {'id':video_id}
        resp=self._api.session.patch(url=url,headers=self._headers,data=payload,files=files if files else None)

        for key in files:
            _,handler,_=files[key]
            handler.close()

        if resp.ok:
            return Video(resp.json())
        else:
            with open('error.html','w',encoding='utf8') as f:
                    f.write(resp.text)
            logger.error('Cant get message from server. PATCH command.info in error.html')
            return None


    def __iter__(self) -> Iterable[Video]:
        return iter(ApiIter(url=self._api.urls.video,headers=self._headers,session=self._api.session,return_class=Video))


    @property
    def videos(self) -> Iterable[Video]:
        return iter(self)

    def __getitem__(self, id)-> Video:
        return self.get(id)
    def __delitem__(self,id):
        return self.delete(id)
