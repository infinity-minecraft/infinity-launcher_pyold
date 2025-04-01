import sys
import re
from PyQt6.QtGui import QGuiApplication
from appstate import build
from PyQt6.QtWidgets import QApplication, QGraphicsLinearLayout, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QSpinBox, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
import configparser
import os
import urllib.request
import webbrowser
import subprocess
import minecraft_launcher_lib


class RunThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        #self.log_signal.emit()
        home_patch = os.path.expanduser("~")
        config = configparser.ConfigParser()
        config.read(f"{home_patch}/.infl/config.ini")
        minecraft_directory = config["GAME"]["minecraftdir"]
        fs = minecraft_launcher_lib.forge.find_forge_version("1.18.2")
        print(fs)
        ram = config["GAME"]["ram"]
        jvma = ["-Xmx2G", f"-Xms{ram}G"]
        nck = config["AUTH"]["nickname"]
        #options = minecraft_launcher_lib.utils.generate_test_options()
        options = {
    
                "username": nck,
                "uuid": nck,
                "token": "",
                "jvmArguments": [f"-Xmx{ram}G", "-Xms2G"]
                }
        print(options)
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.18.2-forge-40.3.0", minecraft_directory, options)
        #minecraft_command = minecraft_launcher_lib.command.get_minecraft_command("1.18.2", minecraft_directory, options)
        print("ll")
        subprocess.run(minecraft_command, cwd=minecraft_directory)
        self.finished_signal.emit()


class InstallThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

    def run(self):
        self.log_signal.emit("Установка игры")
        print("mi_i")
        #self.m_install()
        from install_minecraft import m_install
        m_install()
        home_patch = os.path.expanduser("~")
        configA = configparser.ConfigParser()
        configA.read(f"{home_patch}/.infl/appstate_lastet.ini")
        fb = configA["INFO_S"]["files_ver"]
        print(fb)
        config = configparser.ConfigParser()
        config.read(f"{home_patch}/.infl/config.ini")
        config.set("GAME", "filesversion", f"{fb}")
        with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
            config.write(configfile)
        self.log_signal.emit("Установка игры завершена")
        self.finished_signal.emit()


class MinecraftLauncher(QWidget):
    def __init__(self):
        home_patch = os.path.expanduser("~")
        config = configparser.ConfigParser()
        config.read(f"{home_patch}/.infl/config.ini") 
        super().__init__()
        self.buttonp = False
        self.install_thread = None
        self.log_output = []
        self.username = config["AUTH"]["nickname"]
        self.install_path = config["GAME"]["minecraftdir"]
        self.ram_size = int(config["GAME"]["ram"])  
        self.abuild = build
        self.init_ui()

    def update(self):
        reply = QMessageBox.question(
            self, "Oбновление", "Доступно обновление. Хотите перейти на сайт?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            webbrowser.open("https://github.com/infinity-laucher/infinity/releases/")
            sys.exit()
        else:
            sys.exit()


    def init_ui(self):
        self.setWindowTitle("Infinity launcher")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()
        
        self.label = QLabel("Введите никнейм:")
        layout.addWidget(self.label)
        
        self.username_input = QLineEdit(self.username)
        self.username_input.setPlaceholderText("Ваш ник...")
        layout.addWidget(self.username_input)
        
        self.start_button = QPushButton("Запустить игру")
        self.start_button.clicked.connect(self.launch_game)
        layout.addWidget(self.start_button)
        
        self.settings_button = QPushButton("Настройки")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)
        
        self.fix_button = QPushButton("Починить игру")
        self.fix_button.clicked.connect(self.fix_game)
        layout.addWidget(self.fix_button)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)
        
        self.setLayout(layout)

        self.log_output.append(f"Номер билда: {self.abuild}")

    
    def launch_game(self):
        
        home_patch = os.path.expanduser("~")
        config = configparser.ConfigParser()
        config.read(f"{home_patch}/.infl/config.ini")
        self.username = self.username_input.text().strip()
        config.set("AUTH", "nickname", f"{self.username}")
        with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
            config.write(configfile)
        if self.username:
            if self.buttonp is False:
                self.buttonp = True
                if config["GAME"]["gameinstalled"] == "True":
                    if re.match(r"^\d", f"{self.username}"):
                        self.buttonp = False
                        self.log_output.append(f"Цифры в начале никнейма не разрешены!")
                    else:
                        self.log_output.append(f"Запуск Minecraft для {self.username}...")
                        self.log_output.append(f"Папка установки: {self.install_path if self.install_path else 'Не выбрано'}")
                        self.log_output.append(f"Выделенная память: {self.ram_size} ГБ")
                        self.run_thread = RunThread()
                        self.run_thread.log_signal.connect(self.update_log)
                        self.run_thread.finished_signal.connect(self.run_th)
                        self.run_thread.start()  


                else:
                    self.log_output.append(f"Папка установки: {self.install_path if self.install_path else 'Не выбрано'}")
                    self.install_thread = InstallThread()
                    self.install_thread.log_signal.connect(self.update_log)
                    self.install_thread.finished_signal.connect(self.on_install_finished)
                    #self.log_output.append(f"Установка игры")
                    self.install_thread.start()
                    
            else:
                self.log_output.append("Игра уже запущена/устанавливаеться!")
        else:
            self.log_output.append("Пожалуйста, введите никнейм!")
    
    def run_th(self):
        QMessageBox.information(None, "Запуск игры", "Процес игры был завершен")
        self.buttonp = False

    def update_log(self, message):
        self.log_output.append(message)

    def on_install_finished(self):
        QMessageBox.information(None, "Установка завершена", "Установка игры завершена!")
        self.buttonp = False

    def on_launch(self):
        QMessageBox.information(None, "Игра запущена", "Игра запущена")


    def open_settings(self):
        self.settings_window = QWidget()
        self.settings_window.setWindowTitle("Настройки")
        self.settings_window.setGeometry(150, 150, 400, 200)
        settings_layout = QVBoxLayout()
        
        # Выбор папки установки
        folder_layout = QHBoxLayout()
        folder_label = QLabel("Папка установки:")
        folder_button = QPushButton("Выбрать...")
        folder_button.clicked.connect(self.select_install_folder)
        folder_layout.addWidget(folder_label)
        folder_layout.addWidget(folder_button)
        settings_layout.addLayout(folder_layout)
        
        # Выбор оперативной памяти
        ram_layout = QHBoxLayout()
        ram_label = QLabel("ОЗУ (ГБ):")
        self.ram_input = QSpinBox()
        self.ram_input.setRange(1, 32)  # Выбор от 1 до 32 ГБ
        self.ram_input.setValue(self.ram_size)
        self.ram_input.valueChanged.connect(self.set_ram_size)
        ram_layout.addWidget(ram_label)
        ram_layout.addWidget(self.ram_input)
        settings_layout.addLayout(ram_layout)
        
        self.settings_window.setLayout(settings_layout)
        self.settings_window.show()
    
    def select_install_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку установки")
        if folder:
            self.install_path = folder
            home_patch = os.path.expanduser("~")
            config = configparser.ConfigParser()
            config.read(f"{home_patch}/.infl/config.ini")
            config.set("GAME", "minecraftdir", f"{folder}")
            with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
                config.write(configfile)
            self.log_output.append(f"Выбрана папка установки: {folder}")
    
    def set_ram_size(self, value):
        self.ram_size = value
        self.log_output.append(f"Установлено ОЗУ: {value} ГБ")
        home_patch = os.path.expanduser("~")
        config = configparser.ConfigParser()
        config.read(f"{home_patch}/.infl/config.ini")
        config.set("GAME", "ram", f"{self.ram_size}")
        with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
            config.write(configfile)
    
    def fix_game(self):
        config = configparser.ConfigParser()
        home_patch = os.path.expanduser("~")
        config.read(f"{home_patch}/.infl/config.ini")
        if self.buttonp is False:
            self.buttonp = True
            if not self.install_path:
                QMessageBox.warning(self, "Ошибка", "Не выбрана папка установки!")
                return
            elif config["GAME"]["gameinstalled"] == "False":
                QMessageBox.warning(self, "Ошибка", "Игра не установлена!")
                return
            else:
                self.log_output.append(f"Папка установки: {self.install_path if self.install_path else 'Не выбрано'}")
                self.install_thread = InstallThread()
                self.install_thread.finished_signal.connect(self.on_install_finished)
                self.install_thread.start()
        

    def internet_error(self):
        QMessageBox.information(None, "Internet", "Отсутствует соеденение с интернетом")
        sys.exit()
                
    def update_found(self, launcher):
        QMessageBox.information(None, "Обновление", "Обнаружено обновление для игры. Оно будет устоновленно при следущем запуске")
        launcher.show()

def lauch_ui():
    appstateL = build
    home_patch = os.path.expanduser("~")
    appstate = configparser.ConfigParser()
    try:
        urllib.request.urlretrieve("https://raw.githubusercontent.com/infinity-laucher/state/refs/heads/main/appstate_lastet.ini", f"{home_patch}/.infl/appstate_lastet.ini")
    except:
        app = QGuiApplication(sys.argv)
        launcher = MinecraftLauncher()
        launcher.internet_error()
        sys.exit(app.exec())

    appstate.read(f"{home_patch}/.infl/appstate_lastet.ini")
    appstateS = int(appstate["INFO_S"]["builds"])
    
    print(appstateL)
    print(appstateS)
    if appstateL < appstateS:
        print("update r")
        app = QApplication(sys.argv)
        launcher = MinecraftLauncher()
        launcher.update()
        sys.exit(app.exec())

    else:
        appstateFiles = int(appstate["INFO_S"]["files_ver"])
        appstate.read(f"{home_patch}/.infl/config.ini")
        try:
            appstateFilesl = int(appstate["GAME"]["filesversion"])
        except ValueError:
            print("ve")
            appstate.set("GAME", "gameinstalled", "False")
            with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
                appstate.write(configfile)
            app = QApplication(sys.argv)
            launcher = MinecraftLauncher()
            launcher.update_found(launcher)
            sys.exit(app.exec())
        if appstateFilesl < appstateFiles:
            appstate.set("GAME", "gameinstalled", "False")
            with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
                appstate.write(configfile)
            app = QApplication(sys.argv)
            launcher = MinecraftLauncher()
            launcher.update_found(launcher)
            sys.exit(app.exec())
        else:
            app = QApplication(sys.argv)
            launcher = MinecraftLauncher()
            launcher.show()
            sys.exit(app.exec())


#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    launcher = MinecraftLauncher()
#    launcher.show()
#    sys.exit(app.exec())

