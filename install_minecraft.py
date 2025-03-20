import minecraft_launcher_lib
import os
import configparser


def m_install():
    config = configparser.ConfigParser()
    home_patch = os.path.expanduser("~")
    config.read(f"{home_patch}/.infl/config.ini")
    #forge_version = minecraft_launcher_lib.forge.find_forge_version("1.18.2")
    minecraft_directory = config["GAME"]["minecraftdir"]
    minecraft_launcher_lib.forge.install_forge_version("1.18.2-40.3.0", minecraft_directory)
    config.set("GAME", "gameinstalled", "True")
    with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
        config.write(configfile)


if __name__ == "__main__":
    m_install()

