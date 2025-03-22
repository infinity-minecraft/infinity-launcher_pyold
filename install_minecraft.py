import minecraft_launcher_lib
import os
import configparser
import urllib.request
import zipfile
import shutil


def m_install():
    config = configparser.ConfigParser()
    home_patch = os.path.expanduser("~")
    config.read(f"{home_patch}/.infl/config.ini")
    #forge_version = minecraft_launcher_lib.forge.find_forge_version("1.18.2")
    minecraft_directory = config["GAME"]["minecraftdir"]
    minecraft_launcher_lib.forge.install_forge_version("1.18.2-40.3.0", minecraft_directory)
#    config.set("GAME", "gameinstalled", "True")
#    with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
#        config.write(configfile)
    client_instal(home_patch, config, minecraft_directory)

def client_instal(home_patch, config, minecraft_directory):
    urllib.request.urlretrieve("https://github.com/infinity-laucher/files/archive/refs/heads/main.zip", f"{minecraft_directory}/main.zip") 
    with zipfile.ZipFile(f"{minecraft_directory}/main.zip",'r') as zip_ref:
        zip_ref.extractall(f"{minecraft_directory}")
    source_folder = f"{minecraft_directory}/files-main"
    destination_folder = minecraft_directory
    for root, dirs, files in os.walk(source_folder): 
        relative_path = os.path.relpath(root, source_folder)
        target_path = os.path.join(destination_folder, relative_path)
        os.makedirs(target_path, exist_ok=True)
        for file in files:
            shutil.copy2(os.path.join(root, file), os.path.join(target_path, file))

    shutil.rmtree(f"{minecraft_directory}/files-main/")
    os.remove(f"{minecraft_directory}/main.zip")
    config.read(f"{home_patch}/.infl/config.ini")
    config.set("GAME", "gameinstalled", "True")
    with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
        config.write(configfile)

#    shutil.copytree(f"{minecraft_directory}/files-main", minecraft_directory, dirs_exist_ok=True)
#    os.rename(f"{minecraft_directory}/files-name/*", minecraft_directory)

if __name__ == "__main__":
    m_install()

