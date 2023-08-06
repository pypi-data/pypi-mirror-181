import os
import pydrive
from parse import parse
from .pretrained_checkpoint import FileLocation, PretrainedCheckpoint


def download_file(gdrive,
                  cached_path,
                  progress=True,
                  version='gdown'):
    if gdrive.startswith("https://drive.google.com/open?id="):
        gdrive = parse("https://drive.google.com/open?id={}", gdrive).fixed[0]
    if gdrive.startswith("https://drive.google.com/file/d/"):
        gdrive = parse("https://drive.google.com/file/d/{}", gdrive).fixed[0]

    if version == 'gdown':
        import gdown
        gdown.download(id=gdrive,
                       output=cached_path,
                       quiet=not progress)
    elif version == 'google_drive_downloader':
        from google_drive_downloader import GoogleDriveDownloader as gdd
        gdd.download_file_from_google_drive(file_id=gdrive,
                                            dest_path=cached_path,
                                            showsize=progress)
    else:
        raise NotImplementedError()


def host_file(cached_path,
              folder_id: str,
              overwrite: bool = False):
    from pydrive.auth import GoogleAuth
    from pydrive.drive import GoogleDrive
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
    gfile.SetContentFile(cached_path)
    gfile.Upload()
    file_id = gfile.metadata.get('id') or gfile.get('id')
    return file_id


PretrainedCheckpoint.DOWNLOADERS[FileLocation.GOOGLE_DRIVE] = download_file
PretrainedCheckpoint.UPLOADERS[FileLocation.GOOGLE_DRIVE] = host_file
