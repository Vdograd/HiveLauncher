import os
import requests
from .logger import logger
from .getenv import GetEnv

env = GetEnv()
api_url = env.get_env('GITHUB_URL')
token = env.get_env('GITHUB_TOKEN')

def download():
    logger.info("Search Update-file")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+raw"
    }
    try:
        api_response = requests.get(api_url, headers=headers)
        if api_response.status_code == 200:
            file_info = api_response.json()
            github_file_size = file_info['size']
            download_url = file_info['download_url']
            
            if os.path.exists('Update.exe'):
                local_file_size = os.path.getsize('Update.exe')
                
                if github_file_size != local_file_size:
                    logger.info("Download new update-file")
                    file_response = requests.get(download_url, headers=headers)
                    
                    if file_response.status_code == 200:
                        with open('Update.exe', 'wb') as file:
                            file.write(file_response.content)
                        logger.info('Update-file success updated')
                    else:
                        logger.error(f"Error update setup-update {file_response.status_code}")
            else:
                logger.info("Not found local Update-file. Download with GitHub")
                file_response = requests.get(download_url, headers=headers)
                
                if file_response.status_code == 200:
                    with open('Update.exe', 'wb') as file:
                        file.write(file_response.content)
                    logger.info('Update-file success download')
                else:
                    logger.error(f"Error download setup-update {file_response.status_code}")
        else:
            logger.error(f"Error information from file: {api_response.status_code}")
    except Exception as e:
        raise e