from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

for f in drive.ListFile({'q' : '"root" in parents and trashed = false'}).GetList():
    print(f['title'], '  \t', f['id'])



# file_id = drive.ListFile({'q': 'title = "2020サンマログvol1.txt"'}).GetList()[0]['id']

file_id = '19RVh95KDVvXGL1261fsdHewi4BoSS7Vma30glcg5k68'
# print(file_id)
f = drive.CreateFile({'id': file_id})
f.GetContentFile('download6.txt')

