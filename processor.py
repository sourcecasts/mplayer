# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import threading 
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools
import os
import json
from apiclient.errors import HttpError

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

class Processor(QObject):    # Main Processor check proxy...
    
    length = QtCore.pyqtSignal(str)
    
    def __init__(self, file, title, description):    # Main Processor check proxy...
        super().__init__()
                 
        self.file = file
        self.title = title
        self.description = description


                
    def running(self):
        flow = OAuth2WebServerFlow(
            client_id='509732323643-mb5ctlpgaee3rjgb9cpkl9ln9str01lf.apps.googleusercontent.com',
            client_secret='1tF2q781jKM27FKskH439CVO',
            scope ='https://www.googleapis.com/auth/youtube.upload',
            user_agent ='youtube-api-v3-awesomeness'
        )

        token = 'C:/Users/Скрипт/Desktop/Upload/analytics.dat'

        storage = Storage(token)
        credentials = storage.get()

        api_service_name = "youtube"
        api_version = "v3"

        body = {
            "kind": "youtube#video",
                "snippet": {
                "liveBroadcastContent": "live"
            },
            "snippet": {
                "categoryI": 19,
                "title": self.title,
                "description": self.description,
                "tags": ["Travel", "video test", "Travel Tips"]
            },
            "status": {
                "privacyStatus": "private",
                "selfDeclaredMadeForKids": False, 
            },
            "notifySubscribers": False
        }


        if not credentials or credentials.invalid:
            credentials = tools.run_flow(flow, storage)

        youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials = credentials)
        request = youtube.videos().insert(part='kind,snippet,status', body = body, media_body = MediaFileUpload(self.file, chunksize=-1, resumable=True))
        #response = request.execute()
        #if response:
                #print("Видео загружено")
        self.resumable_upload(request)

          
    def resumable_upload(self, request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Идет загрузка видео...")
                status, response = request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print("Видео загружено", response['id'])
                        self.length.emit(str(response['id']))

                else:
                    exit("Ошибка загрузки")
            except Exception as e:
                print(e)

            if error is not None:
                print (error)
                retry += 1
                if retry > 10:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print("Sleeping %f seconds and then retrying..." % sleep_seconds)
                time.sleep(sleep_seconds)

           
        
           
   
  

   
  