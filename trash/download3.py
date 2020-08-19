import gdown

# url = 'https://drive.google.com/uc?id=0B9P1L--7Wd2vU3VUVlFnbTgtS2c'
# url = "https://docs.google.com/document/d/1szmspIT-yUYmz_tY53wYfa8UIrOuToUwgeYIN2sX274/edit"
# url = "https://docs.google.com/document/d/1szmspIT-yUYmz_tY53wYfa8UIrOuToUwgeYIN2sX274/edit?usp=sharing"
# output = 'download3-1.txt'
# gdown.download(url, output, quiet=False) 

from google_drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(file_id='1szmspIT-yUYmz_tY53wYfa8UIrOuToUwgeYIN2sX274',
                                    dest_path='dwn/download3-2.txt',
                                    unzip=False)