from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QSize
from ...core.version_manager import obj_Version_Manager
import os
import subprocess
from ...utils.logger import logger

def open_window(self, page):
    conf = self.conf
    if page == self.page:
        return
    elif page == 'Home':
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

        self.tab_show_folder_game.setText(obj_Version_Manager.minecraft_directory)
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