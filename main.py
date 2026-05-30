from launcher.utils.download_update import update_file
from launcher.utils.build import build, RestartConfig
from launcher.utils.logger import logger
from launcher.utils.error import ErrorExc
import requests

ErrorExc(requests.exceptions.HTTPError())