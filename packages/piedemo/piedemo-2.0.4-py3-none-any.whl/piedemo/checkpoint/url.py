from torch.hub import download_url_to_file
from .pretrained_checkpoint import FileLocation, PretrainedCheckpoint


def download_file(url,
                  cached_path,
                  progress=True):
    download_url_to_file(url,
                         cached_path,
                         progress=progress)


PretrainedCheckpoint.DOWNLOADERS[FileLocation.URL] = download_file
