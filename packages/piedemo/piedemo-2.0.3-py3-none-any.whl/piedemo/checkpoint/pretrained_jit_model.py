from .pretrained_checkpoint import PretrainedCheckpoint
import torch


class PretrainedJITModel(PretrainedCheckpoint):

    def __init__(self,
                 filename,
                 gdrive=None,
                 url=None,
                 path=None,
                 yadisk=None,
                 mega_path=None,
                 mega_url=None,
                 archive_rel_path=None):
        super(PretrainedJITModel, self).__init__(filename=filename,
                                                 gdrive=gdrive,
                                                 url=url,
                                                 path=path,
                                                 yadisk=yadisk,
                                                 mega_path=mega_path,
                                                 mega_url=mega_url,
                                                 archive_rel_path=archive_rel_path,
                                                 load_function=torch.jit.load)
