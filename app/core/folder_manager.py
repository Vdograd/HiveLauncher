from ..utils.build import build
from pathlib import Path
import re

def get_currect_version() -> str | None:
    directory = Path(build.folders_versions_launcher)
    pattern = r'^\d+(?:#\d+)*+(?:-[a-zA-Z]+)?$'
    versions = []

    for item in directory.iterdir():
        if item.is_dir() and re.match(pattern, item.name):
            mod_time = item.stat().st_mtime
            versions.append((item.name, mod_time))
    
    if not versions:
        return None
    
    versions.sort(key=lambda x: x[1], reverse=True)
    latest_folder = versions[0][0]

    return latest_folder.replace('#', '.')

def get_all_installed_version() -> list | None:
    directory = Path(build.folders_versions_launcher)
    pattern = r'^\d+(?:#\d+)*+(?:-[a-zA-Z]+)?$'
    versions = []

    for item in directory.iterdir():
        if item.is_dir() and re.match(pattern, item.name):
            mod_time = item.stat().st_mtime
            versions.append((item.name, mod_time))
    
    if not versions:
        return None

    return [name[0] for name in versions]
