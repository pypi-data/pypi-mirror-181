import os
from parse import parse
import subprocess
from .pretrained_checkpoint import FileLocation, PretrainedCheckpoint


def host_file(cached_path,
              folder_name: str = 'host_models'):
    """
    curl https://rclone.org/install.sh | sudo bash
    rclone config
    """
    try:
        if "gdrive:" not in subprocess.check_output("rclone listremotes", shell=True).decode('utf-8').strip():
            raise RuntimeError("Configurate rclone:"
                               "rclone config")
    except:
        raise RuntimeError("""Install rclone: 
                        curl https://rclone.org/install.sh | sudo bash
                        rclone config
                    """)

    filename = os.path.basename(cached_path)
    os.system(f"rclone copy -P {cached_path} gdrive:{folder_name}")
    url = subprocess.check_output(f"rclone link gdrive:{folder_name}/{filename}", shell=True).decode('utf-8').strip()
    try:
        file_id = parse("https://drive.google.com/open?id={}", url).fixed[0]
    except:
        raise RuntimeError(f"url has bad format: {url}")
    return file_id


PretrainedCheckpoint.UPLOADERS[FileLocation.RCLONE] = host_file
