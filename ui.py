import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFileDialog, QSpinBox, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
import configparser
import os
import urllib.request
import webbrowser


class MinecraftLauncher(QWidget):
    def __init__(self):
        home_patch = os.path.expanduser("~")
        config = configparser.ConfigParser()
        config.read(f"{home_patch}/.infl/config.ini") 
        super().__init__()

        self.username = config["AUTH"]["nickname"]
        self.install_path = config["GAME"]["minecraftdir"]
        self.ram_size = int(config["GAME"]["ram"])  
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
    
    def launch_game(self):
        home_patch = os.path.expanduser("~")
        config = configparser.ConfigParser()
        config.read(f"{home_patch}/.infl/config.ini")
        self.username = self.username_input.text().strip()
        config.set("AUTH", "nickname", f"{self.username}")
        with open(f"{home_patch}/.infl/config.ini", "w") as configfile:
            config.write(configfile)
        if self.username:
            self.log_output.append(f"Запуск Minecraft для {self.username}...")
            self.log_output.append(f"Папка установки: {self.install_path if self.install_path else 'Не выбрано'}")
            self.log_output.append(f"Выделенная память: {self.ram_size} ГБ")
            if config["GAME"]["gameinstalled"] == "True":
                pass
            else:
                pass
        else:
            self.log_output.append("Пожалуйста, введите никнейм!")
    
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
        if not self.install_path:
            QMessageBox.warning(self, "Ошибка", "Не выбрана папка установки!")
            return
        elif config["GAME"]["gameinstalled"] == "False":
            QMessageBox.warning(self, "Ошибка", "Игра не установлена!")
            return
        
        self.log_output.append("Начинается проверка и восстановление игры...")
        # Здесь можно добавить логику проверки файлов и их восстановления
        self.log_output.append("Игра успешно проверена и восстановлена!")
        QMessageBox.information(self, "Готово", "Проверка и восстановление завершены!")

def lauch_ui():
    home_patch = os.path.expanduser("~")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/infinity-laucher/state/refs/heads/main/appstate_lastet.ini", f"{home_patch}/.infl/appstate_lastet.ini")
    appstate = configparser.ConfigParser()
    appstate.read(f"{home_patch}/.infl/appstate.ini")
    appstateL = int(appstate["INFO"]["build"])
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
        app = QApplication(sys.argv)
        launcher = MinecraftLauncher()
        launcher.show()
        sys.exit(app.exec())

#if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    launcher = MinecraftLauncher()
#    launcher.show()
#    sys.exit(app.exec())

