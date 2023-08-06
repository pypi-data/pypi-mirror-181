import os
from .pretrained_checkpoint import FileLocation, PretrainedCheckpoint
from wldhx.yadisk_direct.main import get_real_direct_link
from torch.hub import download_url_to_file


def download_file(yadisk,
                  cached_path,
                  progress=True):
    url = get_real_direct_link(yadisk)
    download_url_to_file(url,
                         cached_path,
                         progress=progress)


PretrainedCheckpoint.DOWNLOADERS[FileLocation.YANDEX_DISK] = download_file
