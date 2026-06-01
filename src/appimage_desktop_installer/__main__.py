
from argparse import ArgumentParser
import os
import stat
from sys import argv

from . import USER_APP_DIR, monitor_directory, process_appimage, uninstall

parser = ArgumentParser()
parser.add_argument('action', choices=['watch', 'install', 'uninstall'])
parser.add_argument('--install-dir', default=USER_APP_DIR)
parser.add_argument('appimage', nargs='?')

class NotADirectoryError(Exception): ...

def main():
    opts = parser.parse_args(argv[1:])

    if opts.action == 'watch':
        # Ensure the watch directory exists
        if not os.path.exists(opts.install_dir):
            os.makedirs(opts.install_dir, exist_ok=True)
        elif not os.path.isdir(opts.install_dir):
            raise NotADirectoryError(opts.install_dir)
            
        monitor_directory(opts.install_dir)

    elif opts.action == 'install':
        # Make sure the app image exists
        if not os.path.exists(opts.appimage):
            raise FileNotFoundError(opts.appimage)

        filename = os.path.basename(opts.appimage)
        install_path = os.path.join(opts.install_dir, filename)
        if (opts.install_dir != install_path):
            os.rename(opts.appimage, install_path)

        install_stat = os.stat(install_path)
        os.chmod(install_path, install_stat.st_mode | stat.S_IEXEC)

        process_appimage(install_path)
    
    elif opts.action == 'uninstall':
        uninstall(opts.appimage, remove_appimage=True)
    

if __name__ == "__main__": main()
