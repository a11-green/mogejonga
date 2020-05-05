from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
file_id = drive.ListFile({'q': 'title = "log_vol1.txt"'}).GetList()[0]['id']
f = drive.CreateFile({'id': file_id})
f.GetContentFile('download2.txt')