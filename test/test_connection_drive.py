import os
from pathlib import Path
from google.google import GDrive, GSheets

drive = GDrive()
gsheets = GSheets()

df = gsheets.get_data(
     id = "1cI_FrozuLYoK0x3QjmZRtuDkrFYCgaP2gEwdnHpT4Rw"
    ,sheet = "Form responses 1"
)

id = df.iloc[9,3].split("id=")[1]

metadata = drive.get_file_by_id(id)
content = drive.download(id)
with open(metadata["name"], "wb") as f:
    f.write(content)