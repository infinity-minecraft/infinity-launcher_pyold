#import minecraft_launcher_lib
import os
import configparser
from ui import lauch_ui


def start(home_patch):
    check_lock = os.path.exists(f"{home_patch}/.infl/exists.lock")
    if check_lock is True:
        print("Lock file check successful")
        lauch_ui()
    else:
        print("Lock file check failed")
        first_start(home_patch)


def first_start(home_patch):
    os.mkdir(f"{home_patch}/.infl")
    with open(f"{home_patch}/.infl/exists.lock", "w") as f:
        f.close()
    configp = configparser.ConfigParser()
    os.mkdir(f"{home_patch}/.infl/minecraft")
    configp["GAME"] = {"GameInstalled": False,
                       "MinecraftDir": f"{home_patch}/.infl/minecraft",
                       "RAM": 4
                       }
    configp["AUTH"] = {"nickname": "Steve"}
    with open(f'{home_patch}/.infl/config.ini', 'w') as configfile:
        configp.write(configfile)
        configfile.close()

if __name__ == "__main__":
    home_patch = os.path.expanduser("~")
    start(home_patch)

