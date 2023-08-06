import os
from mega import Mega
from .pretrained_checkpoint import FileLocation, PretrainedCheckpoint


def download_file(mega_url,
                  cached_path,
                  progress=True):
    mega = Mega()
    m = mega.login()
    m.download_url(mega_url,
                   dest_path=cached_path)


PretrainedCheckpoint.DOWNLOADERS[FileLocation.MEGA_URL] = download_file
