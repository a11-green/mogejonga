import os
import pprint

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

print(type(drive))
# <class 'pydrive.drive.GoogleDrive'>

f = drive.CreateFile()
print(type(f))
# <class 'pydrive.files.GoogleDriveFile'>

print(f)
# GoogleDriveFile({})

f.SetContentFile('log.txt')
print(f)
# GoogleDriveFile({'title': 'src/lena.jpg', 'mimeType': 'image/jpeg'})

f.Upload()