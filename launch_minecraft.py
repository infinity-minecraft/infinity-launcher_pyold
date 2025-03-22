import minecraft_launcher_lib
import configparser
import os
import subprocess
import sys


def lauch_craft():
    home_patch = os.path.expanduser("~")
    config = configparser.ConfigParser()
    config.read(f"{home_patch}/.infl/config.ini")
    minecraft_directory = config["GAME"]["minecraftdir"]
    ram = int(config["GAME"]["ram"])
    options1["jvmArguments"] = ["-Xmx2G", f"-Xms{ram}G"]
    options = {"username": config["AUTH"]["nickname"]}
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.18.2-40.3.0", minecraft_directory, options, options1)
    subprocess.run(minecraft_command, cwd=minecraft_directory)


