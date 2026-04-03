from ..utils.logger import logger
import shutil
import os
from ..utils.configurator import Configurator
from ..core.version_manager import obj_Version_Manager
conf = Configurator()

def copy_minecraft_files_before_start(version):
    try:
        hotbar_path = None
        command_history_path = None
        options_path = None
        servers_dat_path = None
        servers_dat_old = None

        versions_config = conf.get_installed_versions()
        last_version_used = versions_config['last_version']
        if last_version_used == version: return
        if last_version_used != None:
            path_version_last = obj_Version_Manager.get_version_path(last_version_used)
            if os.path.exists(os.path.join(path_version_last, "hotbar.nbt")):
                hotbar_path = os.path.join(path_version_last, "hotbar.nbt")
            if os.path.exists(os.path.join(path_version_last, "command_history.txt")):
                command_history_path = os.path.join(path_version_last, "command_history.txt")
            if os.path.exists(os.path.join(path_version_last, "options.txt")):
                options_path = os.path.join(path_version_last, "options.txt")
            if os.path.exists(os.path.join(path_version_last, "servers.dat")):
                servers_dat_path = os.path.join(path_version_last, "servers.dat")
            if os.path.exists(os.path.join(path_version_last, "servers.dat_old")):
                servers_dat_old = os.path.join(path_version_last, "servers.dat_old")

            all_files_path = [hotbar_path, command_history_path, options_path, servers_dat_path, servers_dat_old]
            all_files_names = ["hotbar.nbt", "command_history.txt", "options.txt", "servers.dat", "servers.dat_old"]
            path_version_currect = obj_Version_Manager.get_version_path(version)

            for file_path, file_name in zip(all_files_path, all_files_names):
                if file_path == None: continue
                target_path = os.path.join(path_version_currect, file_name)
                shutil.copy2(file_path, target_path)
    except Exception as e:
        logger.error(e)