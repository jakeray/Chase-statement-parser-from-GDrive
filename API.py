# import the required libraries
from __future__ import print_function
import pickle
import os.path
import io
import shutil
from datetime import datetime
import re
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
  
def driveAPI():
    # Define the scopes
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Variable self.creds will
    # store the user access token.
    # If no valid token found
    # we will create one.
    creds = None

    # The file token.pickle stores the
    # user's access and refresh tokens. It is
    # created automatically when the authorization
    # flow completes for the first time.

    # Check if file token.pickle exists
    if os.path.exists('token.pickle'):

        # Read the token from the file and
        # store it in the variable self.creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials are available,
    # request the user to log in.
    if not creds or not creds.valid:

        # If token is expired, it will be refreshed,
        # else, we will request a new one.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle
        # file for future usage
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the API service
    service = build('drive', 'v3', credentials=creds)

    # request a list of first N files or
    # folders with name and id from the API.
    return service

def FileDownload(service, file_id, file_name):
        results = service.files().list(
            pageSize=100, fields="files(id, name)").execute()
        items = results.get('files', [])

        # print a list of files

        print("Here's a list of files: \n")
        print(*items, sep="\n", end="\n\n")
        request = service.files().export(fileId=file_id, mimeType='text/csv')

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%" % int(status.progress() * 100))

    # The file has been downloaded into RAM, now save it in a file
        fh.seek(0)
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(fh, f, length=131072)    


def FileUpload(service, filepath):
    # Extract the file name out of the file path
        head_tail = os.path.split(filepath)
        name = head_tail[1]
            
        # Find the MimeType of the file
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            
        # create file metadata
        file_metadata = {'name': name}

        try:
            media = MediaFileUpload(filepath, mimetype=mimetype)
                
            #Create a new file in the Drive storage
            file = service.files().create(
                body=file_metadata, media_body=media, fields='id').execute()
                
            print("File Uploaded.")
            
        except:
                
            # Raise UploadError if file is not uploaded.
            print("Can't Upload File.")

def StatementUpload(service):
        # Find the MimeType of the file  
        mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'

        statement_directory = r"C:\Users\jacob\Desktop\Coding\Budget\Statements"
        for filename in os.listdir(statement_directory):
            f = os.path.join(statement_directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
            # create file metadata
                
                file_metadata = {'name': NameFile(filename), "parents": ["17FCZOxMSc7UYJd7Ht-Emhps1Yc33_7XX"]}
                try:
                    media = MediaFileUpload(f, mimetype=mimetype)
                        
                    #Create a new file in the Drive storage
                    file = service.files().create(
                       body=file_metadata, media_body=media, fields='id').execute()
                        
                    print("File Uploaded.")
            
                except:
                    # Raise UploadError if file is not uploaded.
                    print("Can't Upload File.")

def NameFile(filename):
    degen = filename.split('_')

    if(filename[5:9] != "7015"):
        tailpipe = degen[len(degen)-2]
    else:
        degen = filename.split('_')
        tailpipe = degen[len(degen)-1]

    datetime_object = datetime.strptime(tailpipe[0:8], '%Y%m%d')
    newname = "Yearly_Statement_as_of_" + datetime_object.strftime("%B%d%Y") + "_ACC" +  filename[5:9] + ".csv"
    
    return newname

def prompt():
    i = int(input("Enter your choice: 1- Download file, 2- Upload File, 3- Upload Statments to Drive, 4- Exit.\n"))
      
    connection = driveAPI()
    if i == 1:
        f_id = input("Enter file id: ")
        f_name = input("Enter file name: ")
        FileDownload(connection,f_id, f_name)
          
    elif i == 2:
        f_path = input("Enter full file path: ")
        FileUpload(connection,f_path)

    elif i == 3:
        StatementUpload(connection)
    else:
        pass