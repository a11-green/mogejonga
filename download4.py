
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
REFERENCES
* [](https://www.it-swarm.dev/ja/python/python-scriptからdropboxにファイルをアップロードする/1047611873/)
* [](https://qiita.com/seigo-pon/items/ca9951dac0b7fa29cce0)
'''
import dropbox

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        """upload a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to,mode=dropbox.files.WriteMode.overwrite)
    
    def download_file(self,file_from,file_to):
        """download a file to Dropbox using API v2
        """
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_to, 'rb') as f:
            dbx.files_download_to_file(file_to, file_from)
    


def upload(file_from,file_to):
    access_token = "GbXhQF7dqhYAAAAAAAAiGOaPGzNPQ4GKcwLWHmsI1VkNR1a-08ZlQ7-a-AvdpeEl"
    transferData = TransferData(access_token)
    # API v2
    transferData.upload_file(file_from, file_to)

def download(file_from,file_to):
    access_token = "GbXhQF7dqhYAAAAAAAAiGOaPGzNPQ4GKcwLWHmsI1VkNR1a-08ZlQ7-a-AvdpeEl"
    transferData = TransferData(access_token)
    # API v2
    transferData.download_file(file_from, file_to)

if __name__ == '__main__':
    # upload()
    download('/logvol1.txt',"log.txt")