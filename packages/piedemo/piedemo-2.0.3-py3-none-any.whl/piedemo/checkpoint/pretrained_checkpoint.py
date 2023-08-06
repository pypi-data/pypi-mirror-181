import os
import torch
from torch.hub import _get_torch_home, download_url_to_file
import enum
from .archive import GeneralArchiveMember


class FileLocation(enum.Enum):
    PATH = 'path'
    GOOGLE_DRIVE = 'google_drive'
    YANDEX_DISK = 'yandex_disk'
    URL = 'url'
    MEGA_PATH = 'mega_path'
    MEGA_URL = 'mega_url'
    RCLONE = 'rclone'


class PretrainedCheckpoint(object):
    DOWNLOADERS = {
    }

    UPLOADERS = {
    }

    def __init__(self,
                 filename,
                 gdrive=None,
                 url=None,
                 path=None,
                 yadisk=None,
                 mega_path=None,
                 mega_url=None,
                 archive_rel_path=None,
                 load_function=torch.load):
        super(PretrainedCheckpoint, self).__init__()
        self.filename = filename
        self.file_location, self.location_path = self.determine_location(gdrive=gdrive,
                                                                         url=url,
                                                                         path=path,
                                                                         yadisk=yadisk,
                                                                         mega_path=mega_path,
                                                                         mega_url=mega_url)
        if archive_rel_path is None:
            archive_rel_path = 'all'
        self.archive_rel_path = archive_rel_path
        self.load_function = load_function

    def determine_location(self,
                           gdrive=None,
                           yadisk=None,
                           path=None,
                           url=None,
                           mega_path=None,
                           mega_url=None):
        if gdrive is not None:
            return FileLocation.GOOGLE_DRIVE, gdrive
        elif url is not None:
            return FileLocation.URL, url
        elif path is not None:
            return FileLocation.PATH, path
        elif yadisk is not None:
            return FileLocation.YANDEX_DISK, yadisk
        elif mega_path is not None:
            return FileLocation.MEGA_PATH, mega_path
        elif mega_url is not None:
            return FileLocation.MEGA_URL, mega_url
        else:
            raise NotImplementedError()

    @staticmethod
    def to_remove_prefix(state_dict, prefix):
        f = lambda x: x.split(prefix, 1)[-1] if x.startswith(prefix) else x
        return {f(key): value for key, value in state_dict.items()}

    @staticmethod
    def to_add_prefix(state_dict, prefix):
        f = lambda x: prefix + x
        return {f(key): value for key, value in state_dict.items()}

    @staticmethod
    def to_replace_prefix(state_dict, replaces,
                          force_startswith=False):
        def f(x):
            for rep_from, rep_to in replaces:
                if not force_startswith or x.startswith(rep_from):
                    x = x.replace(rep_from, rep_to)
            return x
        return {f(key): value for key, value in state_dict.items()}

    @staticmethod
    def postprocess_state_dict(state_dict,
                               pop='state_dict',
                               replaces=None,
                               remove_prefix=None,
                               add_prefix=None):
        data = state_dict
        if pop is not None and isinstance(data, dict) and pop in data:
            data = data[pop]

        if replaces is not None:
            data = PretrainedCheckpoint.to_replace_prefix(data, replaces)

        if remove_prefix is not None:
            data = PretrainedCheckpoint.to_remove_prefix(data, remove_prefix + '.')

        if add_prefix is not None:
            data = PretrainedCheckpoint.to_add_prefix(data, add_prefix + '.')
        return data

    def download(self,
                 model_dir=None,
                 progress=True):
        if model_dir is None:
            torch_home = _get_torch_home()
            model_dir = os.path.join(torch_home, 'checkpoints')

        os.makedirs(model_dir, exist_ok=True)
        cached_path = os.path.join(model_dir, self.filename)
        if not os.path.exists(cached_path):
            self.download_file(cached_path,
                               progress=progress)

        return cached_path

    def load(self,
             map_location='cpu',
             return_path=False,
             model_dir=None,
             progress=True,
             **postprocess):
        cached_path = self.download(model_dir=model_dir,
                                    progress=progress)
        if return_path:
            return cached_path

        state_dict = {}
        if not GeneralArchiveMember.is_archive(cached_path):
            state_dict = self.load_function(cached_path,
                                            map_location=map_location)
        else:
            GA = GeneralArchiveMember(cached_path,
                                      rel_path=self.archive_rel_path)
            with GA.temporary_extract() as ga:
                if self.archive_rel_path == 'all' and len(list(ga.iterdir())) != 1:
                    raise RuntimeError("Please provide archive_rel_path, can't determine which file load")
                elif self.archive_rel_path == 'all':
                    ga = ga / (list(ga.iterdir())[0])
                state_dict = self.load_function(ga,
                                                map_location=map_location)

        state_dict = self.postprocess_state_dict(state_dict, **postprocess)
        return state_dict

    def download_file(self, save_path,
                      progress=True):
        self.DOWNLOADERS[self.file_location](self.location_path,
                                             save_path,
                                             progress)
