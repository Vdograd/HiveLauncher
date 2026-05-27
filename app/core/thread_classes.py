from PyQt6.QtCore import QThread, pyqtSignal
from ..db.db_manager import Manager
from .folder_manager import *
import os
from ..utils.build import build
import pyperclip
from concurrent.futures import ThreadPoolExecutor, as_completed
from ..utils.logger import logger
import time
import shutil
import requests
import threading
import json
from ..utils.Env import Env

class Scanning(QThread):
    error = pyqtSignal(Exception)
    finished = pyqtSignal(int, str)
    start_s = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.dbm = Manager()
        self.token = Env.get_env('GITHUB_TOKEN')
        self.repo_owner = Env.get_env('GITHUB_REPO_OWNER')
        self.repo_name = Env.get_env('GITHUB_REPO_NAME')
        self.branch = Env.get_env('GITHUB_BRANCH')
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.base_url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}'

    def get_github_files(self) -> dict:
        files = {}
        url = f'{self.base_url}/git/trees/{self.branch}?recursive=1'
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('tree', []):
                    if item['type'] == 'blob':
                        normalized_path = str(item['path']).replace('\\', '/')
                        files[normalized_path] = {
                            'sha': item['sha'],
                            'size': item.get('size', 0),
                            'path': normalized_path,
                        }
        except Exception as e:
            logger.warn(f"Error getting GitHub files: {e}")
        return files

    def load_sha_cache(self, version: str) -> dict:
        cache_path = Path(build.folders_versions_launcher) / version.replace('.', '#') / '.installed_sha_cache.json'
        try:
            if cache_path.exists():
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.warn(f"Error loading SHA cache: {e}")
        return {}

    def is_version_installed(self, version: str) -> bool:
        if version is None:
            return False
        
        cache_path = Path(build.folders_versions_launcher) / version.replace('.', '#') / '.installed_sha_cache.json'
        
        if not cache_path.exists():
            logger.info(f"SHA cache not found for version {version}")
            return False
        
        local_cache = self.load_sha_cache(version)
        if not local_cache:
            logger.info(f"SHA cache is empty for version {version}")
            return False
        
        github_files = self.get_github_files()
        if not github_files:
            logger.warn("Failed to get GitHub files, assuming version is installed")
            return True
        
        for file_path, github_info in github_files.items():
            github_sha = github_info.get('sha', '')
            cached_sha = local_cache.get(file_path, '')
            
            if cached_sha != github_sha:
                logger.info(f"SHA mismatch for {file_path}: cached={cached_sha[:8] if cached_sha else 'None'}, github={github_sha[:8] if github_sha else 'None'}")
                return False
        
        logger.info(f"Version {version} is fully installed (all SHA match)")
        return True
    
    def run(self):
        try:
            self.currect_version = get_currect_version() # type: ignore
            self.start_s.emit(f"v{self.currect_version}" if self.currect_version != None else "None")
            self.last_version = self.dbm.get_last_version(0)

            if self.last_version == self.currect_version and self.is_version_installed(self.last_version):
                self.finished.emit(1, self.currect_version)
            else:
                if self.currect_version == None:
                    self.restart_new_update()
                elif not self.is_version_installed(self.currect_version):
                    self.preparing_new_version()
                else:
                    self.preparing_new_version()

        except Exception as e:
            self.error.emit(e)

    def restart_new_update(self) -> None:
        try:
            logger.info('Restart files launcher')
            # Запоминаем файлы конфигурации лаунчера
            files_config = []
            files_name = []
            config_json = os.path.join(build.folders_versions_launcher, '_internal', 'launcher', 'data', 'config.json')
            nicknames_json = os.path.join(build.folders_versions_launcher, '_internal', 'launcher', 'data', 'nicknames.json')
            versions_json = os.path.join(build.folders_versions_launcher, '_internal', 'launcher', 'data', 'versions.json')

            if os.path.exists(config_json):
                files_config.append(config_json)
                files_name.append('config.json')
            if os.path.exists(nicknames_json):
                files_config.append(nicknames_json)
                files_name.append('nicknames.json')
            if os.path.exists(versions_json):
                files_config.append(versions_json)
                files_name.append('versions.json')

            logger.info(f"\ncj: {config_json} {os.path.exists(config_json)}, \nnj: {nicknames_json} {os.path.exists(nicknames_json)}, \nvj: {versions_json} {os.path.exists(versions_json)}")

            # Создаем папку с именем последней версией, заменяя "." на "#"
            vers = self.last_version.replace('.', '#')
            os.makedirs(os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data'), exist_ok=True)

            # Копируем файлы конфигурации в новую версию
            for file_path, file_name in zip(files_config, files_name):
                target_path = os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data', file_name)
                logger.info(f'Copy file in {target_path}')
                shutil.copy2(file_path, target_path)

            # Отправляем на установку новой версии
            self.finished.emit(0, self.last_version)

        except Exception as e:
            self.error.emit(e)
    
    def preparing_new_version(self) -> None:
        logger.info('Preparing new version launcher')
        self.currect_version: str
        try:
            # Запоминаем файлы конфигурации лаунчера
            files_config = []
            files_name = []
            config_json = os.path.join(build.folders_versions_launcher, f'{self.currect_version.replace(".", "#")}', '_internal', 'launcher', 'data', 'config.json')
            nicknames_json = os.path.join(build.folders_versions_launcher, f'{self.currect_version.replace(".", "#")}', '_internal', 'launcher', 'data', 'nicknames.json')
            versions_json = os.path.join(build.folders_versions_launcher, f'{self.currect_version.replace(".", "#")}', '_internal', 'launcher', 'data', 'versions.json')

            if os.path.exists(config_json):
                files_config.append(config_json)
                files_name.append('config.json')
            if os.path.exists(nicknames_json):
                files_config.append(nicknames_json)
                files_name.append('nicknames.json')
            if os.path.exists(versions_json):
                files_config.append(versions_json)
                files_name.append('versions.json')

            logger.info(f"\ncj: {config_json} {os.path.exists(config_json)}, \nnj: {nicknames_json} {os.path.exists(nicknames_json)}, \nvj: {versions_json} {os.path.exists(versions_json)}")

            # Создаем папку с именем последней версией, заменяя "." на "#"
            vers = self.last_version.replace('.', '#')
            os.makedirs(os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data'), exist_ok=True)

            # Копируем файлы конфигурации в новую версию
            for file_path, file_name in zip(files_config, files_name):
                target_path = os.path.join(build.folders_versions_launcher, vers, '_internal', 'launcher', 'data', file_name)
                logger.info(f'Copy file in {target_path}')
                if file_path != target_path:
                    shutil.copy2(file_path, target_path)

            # Отправляем на установку новой версии
            self.finished.emit(0, self.last_version)

        except Exception as e:
            self.error.emit(e)

class StartLauncher(QThread):
    error = pyqtSignal(Exception)
    launcher_open = pyqtSignal(str, str)
    start_download = pyqtSignal(str)
    add_progress = pyqtSignal(int)
    speed_realtime = pyqtSignal(str)
    approximate_time = pyqtSignal(str)
    
    MAX_WORKERS = 8

    def __init__(self, status: int, version: str):
        super().__init__()
        self.status = status
        self.version = version
        self.token = Env.get_env('GITHUB_TOKEN')
        self.repo_owner = Env.get_env('GITHUB_REPO_OWNER')
        self.repo_name = Env.get_env('GITHUB_REPO_NAME')
        self.local_folder = Path(build.folders_versions_launcher) / version.replace('.', '#')
        self.branch = Env.get_env('GITHUB_BRANCH')
        self.session = requests.Session()
        self._stop_event = threading.Event()
        self.session.headers.update({
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        })
        self.base_url = f'https://api.github.com/repos/{self.repo_owner}/{self.repo_name}'
        self.archive_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}
        self.sha_cache_path = self.local_folder / '.installed_sha_cache.json'

        self._bytes_downloaded = 0
        self._total_bytes = 0
        self._download_lock = threading.Lock()
        self._start_time = None
        self._last_speed_update = 0
        self._last_bytes = 0

    def run(self):
        if self.status == 1:
            path = os.path.join(build.folders_versions_launcher, f"{self.version}".replace('.', '#'), 'HiveLauncher.exe')
            self.launcher_open.emit(path, self.version.replace(".", "#"))
        elif self.status == 0:
            self.install_launcher()

    def normalize_path(self, path: Path) -> str:
        return str(path).replace('\\', '/')

    def load_sha_cache(self) -> dict:
        try:
            if self.sha_cache_path.exists():
                with open(self.sha_cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def save_sha_cache(self, cache: dict) -> None:
        try:
            with open(self.sha_cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False)
        except Exception:
            pass

    def get_github_files(self) -> dict:
        files = {}
        url = f'{self.base_url}/git/trees/{self.branch}?recursive=1'
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data.get('tree', []):
                    if item['type'] == 'blob':
                        normalized_path = self.normalize_path(item['path'])
                        files[normalized_path] = {
                            'sha': item['sha'],
                            'size': item['size'],
                            'path': normalized_path,
                            'name': os.path.basename(item['path']),
                            'download_url': f'https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/{self.branch}/{item["path"]}'
                        }
                if data.get('truncated', False):
                    return self._get_github_files_fallback()
            else:
                logger.warn(f"Error Trees API ({response.status_code}), fallback to Contents API")
                return self._get_github_files_fallback()
        except Exception as e:
            logger.warn(f"Error Trees API: {e}, fallback to Contents API")
            return self._get_github_files_fallback()
        return files

    def _get_github_files_fallback(self, path='') -> dict:
        files = {}

        def traverse_directory(current_path):
            url = f'{self.base_url}/contents/{current_path}' if current_path else f'{self.base_url}/contents'
            try:
                response = self.session.get(url, timeout=30)
                if response.status_code == 200:
                    contents = response.json()
                    for item in contents:
                        if item['type'] == 'file':
                            normalized_path = self.normalize_path(item['path'])
                            files[normalized_path] = {
                                'sha': item.get('sha', ''),
                                'size': item['size'],
                                'download_url': item['download_url'],
                                'name': item['name'],
                                'path': normalized_path
                            }
                        elif item['type'] == 'dir':
                            traverse_directory(item['path'])
            except Exception as e:
                logger.warn(f"Error accessing: {e}")

        traverse_directory(path)
        return files

    def get_local_files(self) -> dict:
        files = {}
        self.local_folder.mkdir(parents=True, exist_ok=True)

        for file_path in self.local_folder.rglob('*'):
            if file_path.is_file():
                if file_path.name == '.installed_sha_cache.json':
                    continue
                relative_path = file_path.relative_to(self.local_folder)
                normalized_path = self.normalize_path(relative_path)
                files[normalized_path] = {
                    'size': file_path.stat().st_size,
                    'path': file_path
                }
        return files

    def compare_files(self, github_files: dict, local_files: dict) -> list:
        sha_cache = self.load_sha_cache()
        files_to_download = []
        new_sha_cache = {}

        for file_path, github_info in github_files.items():
            github_sha = github_info.get('sha', '')
            local_info = local_files.get(file_path)

            if local_info is None:
                files_to_download.append({
                    'path': file_path,
                    'reason': 'missing',
                    **github_info
                })
            else:
                cached_sha = sha_cache.get(file_path, '')
                if cached_sha == github_sha:
                    # Файл уже скачан и актуален - сохраняем хэш
                    new_sha_cache[file_path] = github_sha
                elif github_info['size'] != local_info['size'] or cached_sha != github_sha:
                    files_to_download.append({
                        'path': file_path,
                        'reason': 'sha_mismatch',
                        **github_info
                    })
                else:
                    new_sha_cache[file_path] = github_sha

        # Сохраняем только хэши уже существующих актуальных файлов
        self.save_sha_cache(new_sha_cache)
        return files_to_download

    def ensure_directory_exists(self, file_path: str) -> Path:
        full_path = self.local_folder / file_path
        directory = full_path.parent
        directory.mkdir(parents=True, exist_ok=True)
        return full_path

    def format_speed(self, bytes_per_sec: float) -> str:
        if bytes_per_sec < 1024:
            return f"{bytes_per_sec:.1f}B/s"
        elif bytes_per_sec < 1024 ** 2:
            return f"{bytes_per_sec / 1024:.1f}KB/s"
        elif bytes_per_sec < 1024 ** 3:
            return f"{bytes_per_sec / (1024 ** 2):.1f}MB/s"
        elif bytes_per_sec < 1024 ** 4:
            return f"{bytes_per_sec / (1024 ** 3):.1f}GB/s"
        else:
            return f"{bytes_per_sec / (1024 ** 4):.1f}TB/s"

    def format_time(self, seconds: float) -> str:
        if seconds < 0 or seconds == float('inf'):
            return "~ неизвестно"
        
        seconds = int(seconds)
        
        if seconds < 60:
            return f"~ {seconds} секунд"
        elif seconds < 3600:
            minutes = seconds // 60
            if minutes == 1:
                return "~ 1 минута"
            elif 2 <= minutes <= 4:
                return f"~ {minutes} минуты"
            else:
                return f"~ {minutes} минут"
        elif seconds < 86400:
            hours = seconds // 3600
            if hours == 1:
                return "~ 1 час"
            elif 2 <= hours <= 4:
                return f"~ {hours} часа"
            else:
                return f"~ {hours} часов"
        else:
            days = seconds // 86400
            if days == 1:
                return "~ 1 день"
            elif 2 <= days <= 4:
                return f"~ {days} дня"
            else:
                return f"~ {days} дней"

    def update_speed_stats(self, bytes_downloaded: int):
        with self._download_lock:
            self._bytes_downloaded += bytes_downloaded
            
            current_time = time.time()
            
            if current_time - self._last_speed_update >= 0.5:
                elapsed = current_time - self._last_speed_update
                bytes_diff = self._bytes_downloaded - self._last_bytes
                
                if elapsed > 0:
                    speed = bytes_diff / elapsed
                    self.speed_realtime.emit(self.format_speed(speed))
                    
                    remaining_bytes = self._total_bytes - self._bytes_downloaded
                    if speed > 0:
                        remaining_seconds = remaining_bytes / speed
                        self.approximate_time.emit(self.format_time(remaining_seconds))
                    else:
                        self.approximate_time.emit("~ неизвестно")
                
                self._last_speed_update = current_time
                self._last_bytes = self._bytes_downloaded

    def download_file(self, file_info: dict) -> bool | Exception | None:
        if self._stop_event.is_set():
            return
        download_url = file_info['download_url']
        file_path = file_info['path']
        file_sha = file_info.get('sha', '')
        
        try:
            response = self.session.get(download_url, timeout=60)
            if response.status_code == 200:
                local_path = self.ensure_directory_exists(file_path)
                logger.info(f'Download file in: {local_path}')
                
                content = response.content
                with open(local_path, 'wb') as f:
                    f.write(content)
                
                self.update_speed_stats(len(content))
                self._update_sha_cache(file_path, file_sha)
                
                return True
            elif response.status_code != 404:
                logger.warn(f"Error downloading {file_path}: status {response.status_code}")
                return requests.exceptions.HTTPError(f"Status code {response.status_code} for {file_path}")
            else:
                return requests.exceptions.HTTPError(f"Status code {response.status_code} for {file_path}")
        except Exception as e:
            logger.warn(f"Error downloading {file_path}: {e}")
            return e
        
    def _update_sha_cache(self, file_path: str, sha: str) -> None:
        with self._download_lock:
            cache = self.load_sha_cache()
            cache[file_path] = sha
            self.save_sha_cache(cache)

    def install_launcher(self) -> None:
        try:
            self._stop_event.clear()
            self.start_download.emit(self.version)
            github_files = self.get_github_files()
            local_files = self.get_local_files()

            files_to_download = self.compare_files(github_files, local_files)

            if files_to_download:
                total = len(files_to_download)
                downloaded = 0
                failed_files = []
                consecutive_errors = 0
                
                self._bytes_downloaded = 0
                self._total_bytes = sum(f.get('size', 0) for f in files_to_download)
                self._start_time = time.time()
                self._last_speed_update = time.time()
                self._last_bytes = 0

                with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                    futures = {
                        executor.submit(self.download_file, file_info): file_info
                        for file_info in files_to_download
                    }
                    for future in as_completed(futures):
                        if self._stop_event.is_set():
                            executor.shutdown(wait=False, cancel_futures=True)
                            return
                        
                        file_info = futures[future]
                        result = future.result()
                        
                        if result is True:
                            downloaded += 1
                            consecutive_errors = 0
                        else:
                            failed_files.append((file_info, result))
                            consecutive_errors += 1
                            
                            if consecutive_errors >= 3:
                                self._stop_event.set()
                                executor.shutdown(wait=False, cancel_futures=True)
                                self.error.emit(result)
                                return
                        
                        progress = int((downloaded / total) * 100)
                        self.add_progress.emit(progress)

                if failed_files and not self._stop_event.is_set():
                    logger.info(f"Retrying {len(failed_files)} failed files...")
                    
                    for file_info, last_error in failed_files:
                        if self._stop_event.is_set():
                            return
                        
                        result = self.download_file(file_info)
                        
                        if result is True:
                            downloaded += 1
                            progress = int((downloaded / total) * 100)
                            self.add_progress.emit(progress)
                        else:
                            self._stop_event.set()
                            self.error.emit(result)
                            return

            if self._stop_event.is_set():
                return

            # Удаляем папки и файлы прошлых версий
            try:
                files_delete = [
                    os.path.join(build.folders_versions_launcher, '_internal'),
                    os.path.join(build.folders_versions_launcher, '.sync_sha_cache.json'),
                    os.path.join(build.folders_versions_launcher, '.gitignore'),
                    os.path.join(build.folders_versions_launcher, 'HiveLauncher.exe'),
                    os.path.join(build.folders_versions_launcher, 'README.md'),
                    os.path.join(build.folders_versions_launcher, 'LICENSE')
                ]

                for x in files_delete:
                    if os.path.exists(x):
                        if os.path.isdir(x):
                            logger.info(f'Delete folder: {os.path.basename(x)}')
                            shutil.rmtree(x)
                        elif os.path.isfile(x):
                            logger.info(f'Delete file: {os.path.basename(x)}')
                            os.remove(x)
            except Exception as e:
                self.error.emit(e)

            try:
                all_installed_versions = get_all_installed_version()
                if all_installed_versions == None: pass
                else:
                    for version_installed in all_installed_versions:
                        if version_installed == self.version.replace(".", "#"):
                            continue
                        else:
                            logger.info(f'Delete folder: {version_installed}')
                            shutil.rmtree(os.path.join(build.folders_versions_launcher, version_installed))
            except Exception as e:
                self.error.emit(e)

            path = os.path.join(build.folders_versions_launcher, f"{self.version}".replace('.', '#'), 'HiveLauncher.exe')
            self.launcher_open.emit(path, self.version.replace(".", "#"))

        except Exception as e:
            self.error.emit(e)

class CopyLog(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            file = logger.log_file
            with open(file, 'r', encoding="ansi") as f:
                content = f.read()

            pyperclip.copy(content)
        except Exception as e:
            logger.error(e)
        self.finished.emit()
