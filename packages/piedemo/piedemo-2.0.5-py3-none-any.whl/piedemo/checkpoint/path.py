import os
import shutil
from .pretrained_checkpoint import FileLocation, PretrainedCheckpoint


def download_file(path,
                  cached_path,
                  progress=True):
    shutil.copyfile(path, cached_path)


def host_file(cached_path,
              path,
              progress=True):
    shutil.copyfile(cached_path, path)
    return path


PretrainedCheckpoint.DOWNLOADERS[FileLocation.PATH] = download_file
PretrainedCheckpoint.UPLOADERS[FileLocation.PATH] = host_file
