from .logger import logger
from .env import env
import requests
import os

api_url = env.get('GITHUB_URL')
token = env.get('GITHUB_TOKEN')
PATH_UPDATE_FILE = '../Update.exe'

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+raw"
}
    
def update_file() -> None:
    try:
        search_file()
    except Exception as e:
        raise e

def search_file() -> None:
    logger.info("Find the file Update.exe...")

    try:
        api_response = requests.get(api_url, headers=headers)
        if api_response.status_code == 200:
            file_info = api_response.json()
            github_file_size = file_info['size']
            download_url = file_info['download_url']

            if os.path.exists(PATH_UPDATE_FILE):
                local_file_size = os.path.getsize(PATH_UPDATE_FILE)
                if github_file_size != local_file_size:
                    download_file(download_url)
                else:
                    logger.info('Installations Update.exe not required')
            else:
                download_file(download_url)
        else:
            logger.error(f"Failed to retrieve information from Github about the Update.exe file: {api_response.status_code}")
    except Exception as e:
        ...
            
def download_file(download_url: str) -> None:
    logger.info("Install the Update.exe file")

    try:
        file_response = requests.get(download_url, headers=headers)
        if file_response.status_code == 200:
            with open(PATH_UPDATE_FILE, 'wb') as file:
                file.write(file_response.content)
            logger.info('The update.exe file has been successfully installed and is ready to use')
        else:
            logger.error(f"An error occurred while installing the Update.exe file: {file_response.status_code}")
    except Exception as e:
        raise e
    