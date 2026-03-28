from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize
from ...core.version_manager import obj_Version_Manager
import os
import subprocess
from ...utils.logger import logger
from PyQt6.QtWidgets import QFileDialog
from ...utils.helper import Helper
import re
import json
from ..style import set_style
from ..page_functions.page_manager import create_shadow

helper = Helper()
def open_window(self, page):
    conf = self.conf
    if page == self.page:
        return
    elif page == 'Home':
        change_version(self)
        self.home.setIcon(QtGui.QIcon(f"{conf.static_folder}\\action\\home.svg"))
        self.home.show()
        self.account.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\account.svg"))
        self.account.show()
        self.settings.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\settings.svg"))
        self.settings.show()
        self.fon_image.show()
        self.head_nickname.setPixmap(QtGui.QPixmap(self.picture[0]))
        self.head_nickname.show()
        self.nickname_text.setText(self.main.nickname)
        self.nickname_text.show()
        self.button_start.show()
        self.button_open_folder_version.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\folder.svg"))
        self.button_open_folder_version.show()
        self.select_version.show()

        self.panel_base_account.hide()
        self.head_nickname_150.hide()
        self.nickname_text_account.hide()
        self.register_account.hide()
        self.play_time.hide()
        self.text_change_skin.hide()
        self.text_change_cape.hide()
        self.button_load_skin.hide()
        self.button_load_cape.hide()
        self.current_size_skin.hide()
        self.current_size_cape.hide()
        self.button_delete_skin.hide()
        self.button_delete_cape.hide()
        self.button_logout_account.hide()

        self.folder_game_text.hide()
        self.tab_show_folder_game.hide()
        self.edit_folder_game.hide()
        self.size_window_text.hide()
        self.sel_window_size.hide()
        self.after_start_text.hide()
        self.sel_after_start.hide()
        self.rem_text.hide()
        self.sel_rem.hide()
        self.after_download_text.hide()
        self.sel_after_download.hide()
        self.color_theme_text.hide()
        self.sel_color_theme.hide()

        self.page = 'Home'
    elif page == 'Account':
        self.home.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\home.svg"))
        self.account.setIcon(QtGui.QIcon(f"{conf.static_folder}\\action\\account.svg"))
        self.settings.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\settings.svg"))

        self.fon_image.hide()
        self.button_start.hide()
        self.button_open_folder_version.hide()
        self.select_version.hide()

        self.folder_game_text.hide()
        self.tab_show_folder_game.hide()
        self.edit_folder_game.hide()
        self.size_window_text.hide()
        self.sel_window_size.hide()
        self.after_start_text.hide()
        self.sel_after_start.hide()
        self.rem_text.hide()
        self.sel_rem.hide()
        self.after_download_text.hide()
        self.sel_after_download.hide()
        self.color_theme_text.hide()
        self.sel_color_theme.hide()

        self.head_nickname_150.setPixmap(QtGui.QPixmap(self.picture[1]))
        self.nickname_text_account.setText(self.main.nickname)
        dt = self.main.datetime.split("T")[0].split("-")
        self.register_account.setText(f"Зарегистрирован: {dt[2]}.{dt[1]}.{dt[0]}")
        self.play_time.setText(f"Наигранно времени: {round(self.main.play_time, 1)}ч")
        self.panel_base_account.show()
        self.head_nickname_150.show()
        self.nickname_text_account.show()
        self.register_account.show()
        self.play_time.show()
        self.text_change_skin.show()
        self.text_change_cape.show()
        self.button_load_skin.show()
        self.button_load_cape.show()
        self.current_size_skin.show()
        self.current_size_cape.show()
        self.button_delete_skin.show()
        self.button_delete_cape.show()
        self.button_logout_account.show()
    elif page == 'Settings':
        self.home.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\home.svg"))
        self.account.setIcon(QtGui.QIcon(f"{conf.static_folder}\\home\\{conf.get_color_theme()}\\account.svg"))
        self.settings.setIcon(QtGui.QIcon(f"{conf.static_folder}\\action\\settings.svg"))

        self.folder_game_text.show()
        self.tab_show_folder_game.show()
        self.edit_folder_game.show()
        self.size_window_text.show()
        self.sel_window_size.show()
        self.after_start_text.show()
        self.sel_after_start.show()
        self.rem_text.show()
        self.sel_rem.show()
        self.after_download_text.show()
        self.sel_after_download.show()
        self.color_theme_text.show()
        self.sel_color_theme.show()

        self.panel_base_account.hide()
        self.head_nickname_150.hide()
        self.nickname_text_account.hide()
        self.register_account.hide()
        self.play_time.hide()
        self.text_change_skin.hide()
        self.text_change_cape.hide()
        self.button_load_skin.hide()
        self.button_load_cape.hide()
        self.current_size_skin.hide()
        self.current_size_cape.hide()
        self.button_delete_skin.hide()
        self.button_delete_cape.hide()
        self.button_logout_account.hide()

        self.fon_image.hide()
        self.button_start.hide()
        self.button_open_folder_version.hide()
        self.select_version.hide()
    return page

def open_folder_game(self):
    v = self.select_version.currentText()
    logger.info(f'Open folder {v}')
    folder_path = obj_Version_Manager.get_version_path(v)
    try:
        subprocess.Popen(f'explorer "{folder_path}"', shell=True)
    except Exception as e:
        logger.error(f'Failed open folder {v}: {e}')

def auth_fill_data_settings(self):
    self.tab_show_folder_game.setText(obj_Version_Manager.minecraft_directory)
    self.sel_color_theme.addItem("Светлая")
    self.sel_color_theme.addItem("Темная")
    color_th = self.conf.get_color_theme()
    self.sel_color_theme.setCurrentText(f"{'Светлая' if color_th == 'light' else 'Темная'}")

    state = self.conf.get_config()
    for screen in helper.access_screens():
        self.sel_window_size.addItem(screen)
    self.sel_window_size.setCurrentText(state["window_size"])
    for rem in helper.access_rem():
        self.sel_rem.addItem(rem)
    self.sel_rem.setCurrentText(state["maxm"])

    self.sel_after_download.addItem("Ничего")
    self.sel_after_download.addItem("Запустить игру")
    self.sel_after_download.setCurrentText("Ничего" if state["after_download"] == 'nothing' else "Запускать игру")

    self.sel_after_start.addItem("Ничего")
    self.sel_after_start.addItem("Скрыть HiveLauncher")
    self.sel_after_start.addItem("Закрыть HiveLauncher")
    thg = state["after_start"]
    if thg == "nothing":
        xtrd = "Ничего"
    elif thg == "hide":
        xtrd = "Скрыть HiveLauncher"
    elif thg == "close":
        xtrd = "Закрыть HiveLauncher"
    self.sel_after_start.setCurrentText(xtrd)

def changed_window_size(self):
    new_window = self.sel_window_size.currentText()
    window = self.conf.get_config()
    window["window_size"] = new_window
    with open(f"{self.conf.config_folder}\\config.json", "w", encoding="ansi") as file:
        json.dump(window, file, indent=4, ensure_ascii=False)

def changed_rem(self):
    new_rem = self.sel_rem.currentText()
    rem = self.conf.get_config()
    rem["maxm"] = new_rem
    with open(f"{self.conf.config_folder}\\config.json", "w", encoding="ansi") as file:
        json.dump(rem, file, indent=4, ensure_ascii=False)

def changed_after_download(self):
    new_color = self.sel_after_download.currentText()
    color_config = self.conf.get_config()
    if new_color == "Ничего":
        color_new = "nothing"
    elif new_color == "Запустить игру":
        color_new = "start"
    color_config["after_download"] = color_new
    with open(f"{self.conf.config_folder}\\config.json", "w", encoding="ansi") as file:
        json.dump(color_config, file, indent=4, ensure_ascii=False)

def changed_after_start(self):
    new_color = self.sel_after_start.currentText()
    color_config = self.conf.get_config()
    if new_color == "Ничего":
        color_new = "nothing"
    elif new_color == "Скрыть HiveLauncher":
        color_new = "hide"
    elif new_color == "Закрыть HiveLauncher":
        color_new = "close"
    color_config["after_start"] = color_new
    with open(f"{self.conf.config_folder}\\config.json", "w", encoding="ansi") as file:
        json.dump(color_config, file, indent=4, ensure_ascii=False)

def changed_color_theme(self):
    new_color = self.sel_color_theme.currentText()
    color_config = self.conf.get_config()
    color_new = 'light' if new_color == "Светлая" else "dark"
    color_config["color"] = color_new
    with open(f"{self.conf.config_folder}\\config.json", "w", encoding="ansi") as file:
        json.dump(color_config, file, indent=4, ensure_ascii=False)
    state = self.conf.get_color_theme()
    set_style(self.main, state)
    self.button_start.setGraphicsEffect(create_shadow(state))
    self.button_open_folder_version.setGraphicsEffect(create_shadow(state))
    self.panel_base_account.setGraphicsEffect(create_shadow(state))
    self.tab_show_folder_game.setGraphicsEffect(create_shadow(state))
    self.sel_window_size.setGraphicsEffect(create_shadow(state))
    self.sel_after_start.setGraphicsEffect(create_shadow(state))
    self.sel_rem.setGraphicsEffect(create_shadow(state))
    self.sel_after_download.setGraphicsEffect(create_shadow(state))
    self.sel_color_theme.setGraphicsEffect(create_shadow(state))
    update_version_icons(self)

def update_version_icons(self):
    color = self.conf.get_color_theme()
    configurator = self.conf
    for i in range(self.select_version.count()):
        item_text = self.select_version.itemText(i)
        if "Fabric" in item_text:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Normal,QtGui.QIcon.State.On)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.Off)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.On)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.Off)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.On)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.Off)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.On)       
        elif "Minecraft" in item_text:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Normal,QtGui.QIcon.State.On)
            icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.Off)
            icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.On)
            icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.Off)
            icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.On)
            icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.Off)
            icon.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\minecraft.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.On)
        elif "Forge" in item_text:
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Normal,QtGui.QIcon.State.On)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.Off)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Disabled,QtGui.QIcon.State.On)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.Off)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Active,QtGui.QIcon.State.On)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.Off)
            icon1.addPixmap(QtGui.QPixmap(f"{configurator.static_folder}\\home\\{color}\\fabric.svg"), QtGui.QIcon.Mode.Selected,QtGui.QIcon.State.On)       
        self.select_version.setItemIcon(i, icon)

def browse_folder(self):
    folder_path = QFileDialog.getExistingDirectory(
        parent=None,
        caption="Выберите папку",
        directory=obj_Version_Manager.minecraft_directory
    )
    if folder_path:
        obj_Version_Manager.change_minecraft_directory(folder_path.replace("/", "\\"))
        self.tab_show_folder_game.setText(folder_path.replace("/", "\\"))
        change_version(self)
        logger.info(f"Change game_path: {folder_path.replace("/", "\\")}")

def change_version(self):
    version_combobox = self.select_version.currentText()
    version_clear = re.sub(r'[^0-9.-]', '', version_combobox)
    
    if 'Fabric' in version_combobox:
        version_if = version_combobox
    elif 'Forge' in version_combobox:
        version_if = version_combobox
    else:
        version_if = version_clear
    
    version_found = False
    with open(f"{self.conf.config_folder}\\versions.json", "r", encoding="ansi") as file:
        data = json.load(file)
        for vers in data["versions"]:
            if vers == obj_Version_Manager.version_to_folder_json(version_if):
                version_found = True
                break
    
    # Обновляем кнопку запуска
    if not version_found:
        self.button_start.setText("Установить")
    else:
        self.button_start.setText("Запустить")