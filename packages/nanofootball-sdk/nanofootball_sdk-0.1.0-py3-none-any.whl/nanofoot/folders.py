from nanofoot import Api
from nanofoot.constants import ExerciseFolder
import requests
from bs4 import BeautifulSoup


import logging

logger=logging.getLogger('nanofoot.folders')

def get_nfb_folders(html_text:str):
    root=BeautifulSoup(html_text,'html.parser')
    folders_array=[]
    for div in root.find_all('div',{'class':'folder-nfb-elem'}):
        folders_array.append(
                ExerciseFolder(
                main=div.attrs.get('data-id'),
                parent=div.attrs.get('data-parent'),
                short_name=div.attrs.get('data-short'),
                name=div.attrs.get('data-name')
            )
        )
    return folders_array
    

class FolderService:
    def __init__(self, api:Api=None):
        if not api:
            api=Api()
        self._api=api
        self._folders=None
    def get_folders(self) -> list[ExerciseFolder]:
        resp=self._api.request(
            method='get',
            url=self._api.urls.exercises_web_page
        )

        if resp.ok:
            return get_nfb_folders(resp.text)
        logger.error('Cant get folders list')
        return None
    @property
    def folders(self) -> list[ExerciseFolder]:
        if self._folders is None:
            self._folders=self.get_folders()
        return self._folders
    def get_by_short_name(self,short_name:str):
        for folder in self.folders:
            if folder.short_name==short_name:
                return folder
        return None
