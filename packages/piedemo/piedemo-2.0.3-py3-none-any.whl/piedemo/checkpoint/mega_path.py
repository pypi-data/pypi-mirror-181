import os
import platform
from .pretrained_checkpoint import FileLocation, PretrainedCheckpoint


def check_mega():
    if os.system('mega-whoami') != 0:
        print("Download megacmd from https://mega.nz/cmd")
        print("After that mega-login email password")
        print("Add mega to ENVIRONMENT PATH [PATH, /etc/paths]")
        print("or for MacOS: /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell and login email password")


def download_file(mega_path,
                  cached_path,
                  progress=True):
    check_mega()

    if platform.system() == 'Linux':
        os.system('mega-version')
        os.system('mega-speedlimit')
        os.system('mega-df')
    elif platform.system() == 'Darwin':
        os.system('echo version | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
        os.system('echo speedlimit | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
        os.system('echo df | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
    else:
        raise NotImplementedError("Unknow platform")

    if platform.system() == 'Linux':
        os.system(f'mega-get {mega_path} {cached_path}')
    elif platform.system() == 'Darwin':
        cmd = f'echo "get {mega_path} {cached_path}" | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell'
        os.system(cmd)
    else:
        raise NotImplementedError("Unknown platform")


def host_file(cached_path,
              mega_path,
              overwrite=False):

    rel_cached_path = os.path.relpath(cached_path)
    base_dir, name = os.path.split(rel_cached_path)
    check_mega()

    if platform.system() == 'Linux':
        os.system('mega-version')
        os.system('mega-speedlimit')
        os.system('mega-df')
        os.system(f'mega-mkdir -p {base_dir}')
        os.system(f'mega-put {rel_cached_path} {mega_path}')
    elif platform.system() == 'Darwin':
        os.system('echo version | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
        os.system('echo speedlimit | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
        os.system('echo df | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
        os.system(f'echo mkdir -p {base_dir} | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
        os.system(f'echo put {rel_cached_path} {mega_path} | /Applications/MEGAcmd.app/Contents/MacOS/MEGAcmdShell')
    else:
        raise NotImplementedError("Unknow platform")

    return mega_path


PretrainedCheckpoint.DOWNLOADERS[FileLocation.MEGA_PATH] = download_file
PretrainedCheckpoint.UPLOADERS[FileLocation.MEGA_PATH] = host_file
