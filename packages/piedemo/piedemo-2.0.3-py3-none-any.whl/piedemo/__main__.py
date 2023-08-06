import os
import argparse
from .checkpoint import rclone_host_file
from .auto import introspect, import_function
from .webdemo import WebDemo


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='host command',
                                       description="help with checkpoints saving and loading",
                                       dest='command')
    host_parser = subparsers.add_parser('host')
    host_parser.add_argument('path', type=str)

    web_parser = subparsers.add_parser('web')
    web_parser.add_argument('path', type=str)
    web_parser.add_argument('--port', type=int, default=8008)
    web_parser.add_argument('--host', type=str, default='0.0.0.0')
    web_parser.add_argument('--inrow', action='store_true')
    web_parser.add_argument('--incol', action='store_true')

    args = parser.parse_args()
    return args


def execute(command, path,
            port=8008,
            host='0.0.0.0',
            inrow=False,
            incol=False):
    if command == 'host':
        print("Host model option")
        gdrive = rclone_host_file(path)
        filename = os.path.basename(path)
        print("Url: ")
        print(f"https://drive.google.com/open?id={gdrive}")
        print("Filename: ")
        print(filename)
        print("Code:")
        print(f"PretrainedCheckpoint(gdrive='{gdrive}',\n"
              f"                     filename='{filename}')")

    elif command == 'web':
        fn, name = import_function(path)
        kwargs = introspect(fn,
                            inrow=inrow,
                            incol=incol)
        kwargs.update({"name": name})
        web = WebDemo(**kwargs)
        web.run(host=host, port=port)


if __name__ == "__main__":
    execute(**vars(parse_args()))
