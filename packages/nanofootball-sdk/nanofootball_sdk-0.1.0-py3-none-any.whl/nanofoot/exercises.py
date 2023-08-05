from typing import Callable,Iterable,Iterator

from .api import Api
from .constants import __BASIC__SCHEME__,ExerciseFolder
from .folders import FolderService
import logging
import re
logger=logging.getLogger('nanofoot.exercises')

def tryparse_int(value,on_error=None):
    try:
        return int(value)
    except Exception:
        return on_error


class ApiRequestError(Exception):
    pass

class ExerciseInfo:
    def __init__(self, data:dict):
        self.raw_data=data
    @property
    def description(self):
        return self.raw_data.get('description')
    @property
    def id(self):
        return self.raw_data.get('id')
    @property
    def title(self):
        return self.raw_data.get('title')
    @property
    def folder(self):
        return ExerciseFolder(
            main=self.raw_data.get('folder_id'),
            parent=self.raw_data.get('folder_parent_id'))
    @property
    def ref_goal(self):
        return self.raw_data.get('ref_goal')
    @property
    def ref_ball(self):
        return self.raw_data.get('ref_ball')
    @property
    def ref_team_category(self):
        return self.raw_data.get('ref_team_category')
    @property
    def ref_age_category(self):
        return self.raw_data.get('ref_age_category')
    @property
    def ref_cognitive_load(self):
        return self.raw_data.get('ref_cognitive_load')
    @property
    def ref_train_part(self):
        return self.raw_data.get('ref_train_part')
    @property
    def scheme_data(self):
        return self.raw_data.get('scheme_data')
    @property
    def video_1(self):
        if self.raw_data.get('video_1'):
            return int(self.raw_data.get('video_1').get('id'))
        else:
            return None
    @property
    def video_2(self):
        if self.raw_data.get('video_2'):
            return int(self.raw_data.get('video_2').get('id'))
        else:
            return None
    @property
    def animation_1(self):
        if self.raw_data.get('animation_1'):
            return int(self.raw_data.get('animation_1').get('id'))
        else:
            return None
    @property
    def animation_2(self):
        if self.raw_data.get('animation_2'):
            return int(self.raw_data.get('animation_2').get('id'))
        else:
            return None
    @property
    def video_ids(self):
        """returns list of video and animation ids in this exercise"""
        fields=['animation_1','animation_2','video_1','video_2']
        return [getattr(self,field) for field in fields if getattr(self,field)!=-1 and getattr(self,field) is not None] # if not -1 than it is not exist
    @property
    def has_videos(self):
        return True if self.video_ids else False
    
    def find_video_place(self,video_id):
        fields=['animation_1','animation_2','video_1','video_2']
        return [field for field in fields if str(getattr(self,field))==str(video_id)]

    

def _parse_exercise_response(text:str):
    pattern=r'\[(?P<exs_id>\d+)\]'
    match=re.search(pattern,text)
    if match:
        return match.group('exs_id')
    else:
        logger.error(f'cant parse exercise id from string "{text}"')
        return None

class ExerciseListIter:
    """returns an iterator over the list of exercise ids

    ids_list: iterator over exercise ids (ex: iter([122,322,123,]))
    create_function: a function that receives a exercise id and returns ExerciseInfo object
        
    NOTE: eit returns ExerciseInfo object from list of ids,
    so every iterations ends up with a request to a server"""

    def __init__(self, ids_iter : list[int],create_function : Callable[[int],ExerciseInfo]):
        self._iter=ids_iter
        self._creator_func=create_function
    
    def __iter__(self) -> Iterable[ExerciseInfo]:
        return self
    
    def __next__(self) -> ExerciseInfo:
        next_id=next(self._iter)
        return self._creator_func(next_id)

class ExercisesIdsIter:
    """A class iterating over each folder and returns all exercises ids"""
    # needed for Exercises['*']
    pass



class ExercisesService:
    """A class for working with exercises, updating, deleting, creating, listing"""
    def __init__(self, api:Api=None):
        if not api:
            api=Api()
        self._api=api


    def delete_exercise(self,exs_id,type_:str='nfb_folders',with_video=False):
        """deleteting exercise
        exs_id: exercise id to delete
        with_video: also deletes video if True(defaults to False)
        returns server response json is ok
        """
        if with_video:
            delete_type=2
        else:
            delete_type=0
        return self._delete_exercise(exs_id=exs_id,type_=type_,delete_type=delete_type)

    def delete_videos_from_exercise(self,exs_id,type_:str='nfb_folders'):
        """deleteting only videos from exercise
        exs_id: exercise id
        returns server response json is ok
        """
        delete_type=1
        return self._delete_exercise(exs_id=exs_id,type_=type_,delete_type=delete_type)

    def _delete_exercise(self,exs_id,type_:str = 'nfb_folders', delete_type=0):
        """inner function for deleting exercise
        exercise id: exercise id
        delete_type: 
            0 for deleting only exercise
            1 deleting only videos, exercise stays
            2 deleting video with exercise
        returns server response json is ok
        """
        if delete_type not in range(3):  # only 0,1,2 values are allowed
            raise AttributeError('delete type must be in 0..2')

        payload={
            #'token':self._api.token,
            'delete_exs': 1,
            'exs':exs_id,
            'type':type_,
            'delete_type':delete_type
            }

        headers={
            'X-CSRFToken':self._api.csrf_token,
            'X-Requested-With': 'XMLHttpRequest' ### именно в этом апи такой заголовок важен для /exercises/exercises_api
        } 

        resp=self._api.session.post(
            url=self._api.urls.exercises,
            data=payload,
            headers=headers)
          
        if not resp.ok:
            with open('error.html','w',encoding='utf8') as f:
                f.write(resp.text)
                #logger.error('dumped to error.html')
            raise ApiRequestError(f'error deleting {exs_id}. more info in error.html')
        resp_json=resp.json()
        if not resp_json['success']==True:
            raise ApiRequestError(f'server returned success!=true for exercise {exs_id}')

        if resp.status_code==200: #OK
            return resp_json
        else:
            logger.warn(f'Some stuff with delete. Must be status code 200 but its {resp.status_code}')
            return resp_json


    def get(self, exs_id,get_nfb=1,f_type='nfb_folders') -> ExerciseInfo:
        payload={
            #'token':self._api.token,
            'get_exs_one': 1,
            'exs':exs_id,
            'f_type':f_type,
            'get_nfb':get_nfb
            }

        headers={
            'X-CSRFToken':self._api.csrf_token,
            'X-Requested-With': 'XMLHttpRequest' ### именно в этом апи такой заголовок важен для /exercises/exercises_api
        } 

        resp=self._api.session.get(
            url=self._api.urls.exercises,
            params=payload,
            headers=headers) 

        if resp.ok:
            resp_json:dict=resp.json()       
            if resp_json.get('success'):
                return ExerciseInfo(resp_json.get('data'))

        logger.error(f'Cant get exercise {exs_id}: {resp.text}')
        return None
        
    def create_exercise(self,title:str,folder:ExerciseFolder,description='',type='nfb_folders',videos:list=[],animations:list=[]):
        if len(videos)>2 or len(animations)>2:
            raise Exception('Too much videos or animation. Maximun 2 allowed')

        payload={
            #'token':self._api.token,
            'edit_exs':1,
            'type':type,
            'data[folder_parent]': folder.parent,
            'data[folder_main]': folder.main,
            'data[ref_goal]': '',
            'data[ref_ball]': '',
            'data[ref_team_category]': '',
            'data[ref_age_category]': '',
            'data[ref_train_part]': '',
            'data[ref_cognitive_load]': '',
            'data[title]': title,
            'data[description]': description,
            'data[scheme_1]':__BASIC__SCHEME__,
            'data[scheme_2]': __BASIC__SCHEME__,
            'data[video_1]': videos[0] if len(videos)>0 else '',
            'data[video_2]': videos[1] if len(videos)>1 else '', 
            'data[animation_1]':animations[0] if len(animations)>0 else '',
            'data[animation_2]':animations[1] if len(animations)>1 else '' 
            
        }

        headers={
            'X-CSRFToken':self._api.csrf_token,
            'X-Requested-With': 'XMLHttpRequest' ### именно в этом апи такой заголовок важен для /exercises/exercises_api
        } 
        import requests
        resp=self._api.session.post(
            url=self._api.urls.exercises,
            data=payload,
            headers=headers)
          
        if not resp.ok:
            try:
                data=resp.json()
                err=data['err'] or data['detail']
                exception= ApiRequestError(f'Error creating exercise: {err}')
            except:
                with open('error.html','w',encoding='utf8') as f:
                    f.write(resp.text)
                #logger.error('dumped to error.html')
                exception= ApiRequestError(f'Uncnown error creating exercise. More info in error.html')
            raise exception

        if resp.status_code==200: #OK
            return _parse_exercise_response(resp.text)
        else:
            logger.warn(f'Some stuff with delete. Must be status code 200 but its {resp.status_code}')
            return _parse_exercise_response(resp.text)
    
    def patch(self, exs_id, type_='nfb_folders', **kwargs):
        exs_info=self.get(exs_id=exs_id)
        payload={
            'edit_exs': 1,
            'exs':exs_id,
            'type':type_,
            'data[folder_parent]': exs_info.folder.parent,
            'data[folder_main]': exs_info.folder.main,
            'data[ref_goal]': exs_info.ref_goal,
            'data[ref_ball]': exs_info.ref_ball,
            'data[ref_team_category]': exs_info.ref_team_category,
            'data[ref_age_category]': exs_info.ref_age_category,
            'data[ref_train_part]': exs_info.ref_train_part,
            'data[ref_cognitive_load]': exs_info.ref_cognitive_load,
            'data[title]': exs_info.title,
            'data[description]': exs_info.description,
            'data[scheme_1]':exs_info.scheme_data[0],
            'data[scheme_2]':exs_info.scheme_data[1],
            'data[video_1]': exs_info.video_1 if exs_info.video_1!=-1 else '',
            'data[video_2]': exs_info.video_2 if exs_info.video_2!=-1 else '', 
            'data[animation_1]' : exs_info.animation_1 if exs_info.animation_1!=-1 else '',
            'data[animation_2]' : exs_info.animation_2 if exs_info.animation_2!=-1 else ''
            }

        #populating with updates
        for key in kwargs:
            payload[f'data[{key}]']=kwargs[key]

        headers={
            'X-CSRFToken':self._api.csrf_token,
            'X-Requested-With': 'XMLHttpRequest' ### именно в этом апи такой заголовок важен для /exercises/exercises_api
        } 

        resp=self._api.session.post(
            url=self._api.urls.exercises,
            data=payload,
            headers=headers)
        
        if resp.ok:
            if resp.json().get('success'):
                return True
        logger.warn(f'update exercise failed:{resp.text}')
        return False

    def list_folder(self,folder:ExerciseFolder,get_nfb=1,f_type='nfb_folders') -> list[ExerciseInfo]:
        payload={
            'get_exs_all': 1,
            'folder':folder.main,
            'f_type':f_type,
            'get_nfb':get_nfb
            }

        headers={
            'X-CSRFToken':self._api.csrf_token,
            'X-Requested-With': 'XMLHttpRequest' ### именно в этом апи такой заголовок важен для /exercises/exercises_api
        } 

        resp=self._api.session.get(
            url=self._api.urls.exercises,
            params=payload,
            headers=headers)
        
        if resp.ok:
            resp_json=resp.json()
            if resp_json.get('success'):
                exercise_ids=[data['id'] for data in resp_json.get('data')]
                return iter(ExerciseListIter(ids_iter=iter(exercise_ids),create_function=self.get))
              # return #[self.get(data['id']) for data in resp_json.get('data')] # so api doent return some classic data, we nned to get if by another request
        logger.warn(f'List folder {folder} failed:{resp.text}')
        return False       

    def __getitem__(self, item):
        """ returns an ExerciseInfo object or iterator over list of exercises
        item: if can be int returns an single object, if its a string like folder, returns a list of Exercises in that folder
        """
        index=tryparse_int(item)
        if index is not None:
            return self.get(exs_id=index)
        else:
            folder=FolderService(api=self._api).get_by_short_name(item)
            if not folder:
                raise IndexError(f'Folder {item} not found')
            return self.list_folder(folder=folder)
