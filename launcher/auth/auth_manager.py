import json
import datetime
from supabase import create_client, Client
from ..utils.configurator import Configurator
from .auth_verify import AuthVerify
from .encryption import encryption_password
from dotenv import load_dotenv
import os

class AuthManager:
    def __init__(self):
        load_dotenv()
        self.verify = AuthVerify()
        self.configurator = Configurator()
        self.supabase: Client = create_client(
            os.getenv('DATABASE_URL'),
            os.getenv('API_KEY')
        )
    
    def initial_database(self):
        """Снижаем задержку выполнения sql-запросов"""
        try:
            self.supabase.table("Users").select("nickname").limit(1).execute()
        except Exception as e:
            return e

    def create_user(self, nickname, password):
        password = encryption_password(password)
        verify_code_for_nickname = self.verify.generate_verify_code(nickname)
        try:
            reg_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            reg_f = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            self.supabase.table("Users").insert(
                {
                    "nickname":f"{nickname}", 
                    "password": f"{password}", 
                    "play_time": 0.0, 
                    "register_time": reg_time,
                    "verify_code": verify_code_for_nickname
                }
            ).execute()
            with open(f"{self.configurator.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
                data = json.load(file)
            with open(f"{self.configurator.config_folder}\\nicknames.json", "w", encoding="ansi") as file_w:
                data["verify_code"][nickname] = verify_code_for_nickname
                data["nicknames"].append(nickname)
                data["last_nickname"] = nickname
                json.dump(data, file_w, indent=4, ensure_ascii=False)
            return (nickname, 0.0, reg_f)
        except Exception as e:
            if "duplicate key value violates unique constraint" in str(e):
                return "Nickname dublicate"
            else:
                return e
            
    def list_nicknames(self):
        try:
            with open(f"{self.configurator.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
                data = json.load(file)
            nicknames = data["nicknames"]
            all_users = []
            for name in nicknames:
                try:
                    verify_code = data["verify_code"][name]
                except Exception as e:
                    return e
                try:
                    verify_code_from_database = self.supabase.table("Users").select("verify_code").eq("nickname", name).execute().data[0]['verify_code']
                except Exception as e:
                    return e
                if verify_code == verify_code_from_database:
                    all_users += [[name, "success"]]
                else:
                    all_users += [[name, "failed"]]
            return all_users
        except Exception as e:
            return e
    
    def auth_in_account(self, nickname, password):
        try:
            verify_code_for_nickname = self.verify.generate_verify_code(nickname)
            password = encryption_password(password)

            with open(f"{self.configurator.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
                data = json.load(file)
            if nickname in data["nicknames"]:
                return "Account already added"
            try:
                user_from_database = self.supabase.table("Users").select("*").eq("nickname", nickname).execute()
            except Exception as e:
                return e
            if user_from_database.data == []:
                return "Not found nickname in db"
            if password == user_from_database.data[0]['password']:
                if user_from_database.data[0]["verify_code"] != verify_code_for_nickname:
                    try:
                        self.supabase.table("Users").update({"verify_code": verify_code_for_nickname}).eq("nickname", nickname).execute()
                    except Exception as e:
                        return e
                with open(f"{self.configurator.config_folder}\\nicknames.json", "w", encoding="ansi") as file_w:
                    data["verify_code"][nickname] = verify_code_for_nickname
                    data["nicknames"].append(nickname)
                    data["last_nickname"] = nickname
                    json.dump(data, file_w, indent=4, ensure_ascii=False)
                return (user_from_database.data[0]["nickname"], user_from_database.data[0]["play_time"], user_from_database.data[0]["register_time"])
            else:
                return "Not correct password"
        except Exception as e:
            return e
        
    def auth_in_account_retry(self, nickname, password):
        try:
            verify_code_for_nickname = self.verify.generate_verify_code(nickname)
            password = encryption_password(password)
            with open(f"{self.configurator.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
                data = json.load(file)
            try:
                user_from_database = self.supabase.table("Users").select("*").eq("nickname", nickname).execute()
            except Exception as e:
                return e
            if user_from_database.data == []:
                return "Not found nickname in db"
            if password == user_from_database.data[0]['password']:
                try:
                    self.supabase.table("Users").update({"verify_code": verify_code_for_nickname}).eq("nickname", nickname).execute()
                except Exception as e:
                    return e
                with open(f"{self.configurator.config_folder}\\nicknames.json", "w", encoding="ansi") as file_w:
                    data["verify_code"][nickname] = verify_code_for_nickname
                    data["last_nickname"] = nickname
                    json.dump(data, file_w, indent=4, ensure_ascii=False)
                return (user_from_database.data[0]["nickname"], user_from_database.data[0]["play_time"], user_from_database.data[0]["register_time"])
            else:
                return "Not correct password"
        except Exception as e:
            return e
        
    def exit_with_account(self, nickname):
        try:
            with open(f"{self.configurator.config_folder}\\nicknames.json", "r", encoding="ansi") as file:
                data = json.load(file)
            with open(f"{self.configurator.config_folder}\\nicknames.json", "w", encoding="ansi") as file_w:
                data["verify_code"][nickname] = "log in again"
                json.dump(data, file_w, indent=4, ensure_ascii=False)
        except Exception as e:
            return e
        return "Success logout"
    
    def update_play_time(self, nickname, play_time_plus: float):
        try:
            current_time = float(self.supabase.table("Users").select("play_time").eq("nickname", nickname).execute().data[0]['play_time'])
        except Exception as e:
            return e
        try:
            self.supabase.table("Users").update({"play_time": current_time+play_time_plus}).eq("nickname", nickname).execute()
        except Exception as e:
            return e
        return current_time + play_time_plus
    
    def select_data_user(self, nickname):
        try:
            user_from_database = self.supabase.table("Users").select("*").eq("nickname", nickname).execute()
        except Exception as e:
            return e
        return (user_from_database.data[0]["nickname"], user_from_database.data[0]["play_time"], user_from_database.data[0]["register_time"])