import os
import sys
from pathlib import Path


def user_config_dir(app: str = "", platform: str = sys.platform):
    dir = ""
    match platform:
        case "win32":
            dir = os.getenv("AppData")
            if dir is None:
                dir = os.getenv("UserProfile")
                if dir is None:
                    raise "neither %AppData% nor %UserProfile% are defined"
            if app != "":
                dir = Path(dir).joinpath(app)
            return dir

        case "darwin":
            dir = os.getenv("HOME")
            if dir is None:
                raise "$HOME is not defined"
            dir = Path(dir)
            dir = dir.joinpath("/Libary/Application Support")
            if app != "":
                dir = dir.joinpath(app)
            return str(dir)

        case "linux":
            dir = os.getenv("XDG_CONFIG_HOME")
            if dir is None:
                dir = os.getenv("HOME")
                if dir is None:
                    raise "neither $XDG_CONFIG_HOME nor $HOME are defined"
                dir = Path(dir)
                dir = dir.joinpath(".config")
                if app != "":
                    dir = dir.joinpath(app)
            return str(dir)

        case _:
            raise "Your platform is not supproted. Currently, dirlib supports Windows, Unix and macOS"
