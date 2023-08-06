import os
from pathlib import Path
import bz2
import zipfile
import tarfile
import tempfile


class GeneralArchiveMember(object):
    def __init__(self, archive_path,
                 rel_path='all'):
        archive_path = Path(archive_path)
        self.archive_path = archive_path
        if archive_path.suffix.lower() == '.bz2':
            ArchiveFile = bz2.BZ2File
        elif archive_path.suffix.lower() == '.zip':
            ArchiveFile = zipfile.ZipFile
        elif ''.join(archive_path.suffixes).lower().endswith('.tar.gz'):
            ArchiveFile = lambda name: tarfile.open(name, 'r:gz')
        else:
            raise NotImplementedError(f"archive_path={archive_path}")

        self.ArchiveFile = ArchiveFile

        self.temp_dir = None
        self.archive_file = None

        self.rel_path = rel_path

    @staticmethod
    def is_archive(path):
        path = Path(path)
        if path.suffix.lower() == '.bz2':
            return True
        elif path.suffix.lower() == '.zip':
            return True
        elif ''.join(path.suffixes).lower().endswith('.tar.gz'):
            return True

        return False

    def temporary_extract(self):
        return self

    def __enter__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.archive_file = self.ArchiveFile(str(self.archive_path))

        temp_dir = self.temp_dir.__enter__()
        archive_file = self.archive_file.__enter__()

        if self.ArchiveFile is bz2.BZ2File:
            data = archive_file.read()
            ckpt_path = os.path.join(temp_dir, str(self.archive_path)[:-4])
            with open(ckpt_path, 'wb') as fout:
                fout.write(data)
        else:
            if self.rel_path == 'all':
                archive_file.extractall(temp_dir)
            else:
                try:
                    archive_file.extract(self.rel_path, temp_dir)
                except:
                    print(self.listarchive())
                    raise

            if self.rel_path == 'all':
                ckpt_path = self.temp_dir
            else:
                ckpt_path = os.path.join(temp_dir, self.rel_path)
        return Path(ckpt_path)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp_dir.__exit__(exc_type, exc_val, exc_tb)
        self.temp_dir = None
        self.archive_file.__exit__(exc_type, exc_val, exc_tb)
        self.archive_file = None

    def listarchive(self):
        if self.ArchiveFile is bz2.BZ2File:
            return [str(self.archive_path.name)[:-4]]
        else:
            with self.ArchiveFile(str(self.archive_path)) as archive_file:
                if self.ArchiveFile is tarfile.TarFile:
                    return archive_file.list()
                elif self.ArchiveFile is zipfile.ZipFile:
                    return list(map(lambda x: x.filename, archive_file.filelist))
                else:
                    raise NotImplementedError()
