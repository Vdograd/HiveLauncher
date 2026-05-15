from supabase import create_client, Client
from ..utils.Env import Env

class Manager:
    def __init__(self):
        self.supabase: Client = create_client(
            Env.get_env('DATABASE_URL'),
            Env.get_env('API_KEY')
        )

    def get_last_version(self, type: int) -> str:
        try:
            versions = self.supabase.table("Launcher_Versions").select("version").eq("type", type).execute().data
            return versions[-1]['version'] # type: ignore
        except Exception as e:
            raise e