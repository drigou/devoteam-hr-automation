import os
from pathlib import Path
import io
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

project_path = Path(os.getcwd())

# Scope also needed for downloading files
SCOPES = [ "https://www.googleapis.com/auth/drive"
          ]

def authenticate(refresh=False):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                project_path / "google_client_cred.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())

    return creds



class GDrive:
    def __init__(self):
       self.service = self.connect()

    def authenticate():
       pass 
    
    def connect(self):
        return build("drive", "v3", credentials=authenticate())
    
    def search_files(self):
        return self.service.files().list().execute()["files"]
    
    def search_folders(self):
        return list(filter(lambda f: f["mimeType"][::-1].split(".")[0][::-1]=="folder", self.search_files()))
    
    def get_file_by_id(self, id, fields=[]):
        if len(fields) == 0:
            fields = ["kind", "id", "name", "mimeType"]
        return self.service.files().get(
                        fileId=id, 
                        fields=",".join(fields)
                    ).execute()
    
    def download(self, id):
        try:
            request = self.service.files().get_media(fileId=id)
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)

            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}.")

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        return file.getvalue()
    

class GSheets:
    def __init__(self):
        self.service = self.connect()
        
    def connect(self):
        return build("sheets", "v4", credentials=authenticate())
    
    def get_data(self, id, sheet, range=None):
        # Set the range
        range = "1!A1:E100000" if range is None else range
        sheet_range = sheet + "!" + range

        # Get the data
        response = self.service.spreadsheets().values() \
            .get(spreadsheetId="1cI_FrozuLYoK0x3QjmZRtuDkrFYCgaP2gEwdnHpT4Rw", range="Form responses 1!A1:E100000") \
            .execute() \
            .get("values")
        
        # Get the data
        n_cols = len(response[0])
        data = [i + (['']*(n_cols-len(i))) for i in response[1:]]

        return pd.DataFrame(data, columns=response[0])

