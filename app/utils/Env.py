import os
from dotenv import load_dotenv

class GetEnv:
    def __init__(self):
        load_dotenv()
    def get_env(self, key: str) -> str:
        return str(os.getenv(key))
    
Env = GetEnv()