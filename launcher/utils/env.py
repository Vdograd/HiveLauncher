from dotenv import load_dotenv
import os

class GetEnv:
    def __init__(self):
        load_dotenv()
    def get(self, key) -> str:
        data = os.getenv(key)
        if data != None: return data
        else:
            raise ValueError('Failed to load .env by key')
    
env = GetEnv()