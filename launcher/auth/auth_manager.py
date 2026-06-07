from ..utils.error_manager.error_classes import DataBaseError, UserAlreadyExistsError, UserNotFoundError, UserAlreadyAddedError, NotCorrectPasswordError, VaildEmailError
from supabase import create_client, Client
from .auth_verify import auth_verify
from ..utils.logger import logger
from ..utils.helper import helper
from ..utils.build import build
from ..utils.env import env
import datetime
import pathlib
import json
import os

class AuthManager:
    def __init__(self): 
        self.supabase: Client = create_client(env.get('DATABASE_URL'), env.get('API_KEY'))

    def initial_database(self) -> None:
        try:
            self.supabase.table("Users").select("nickname").limit(1).execute()
        except Exception as e:
            raise DataBaseError(e)
    
    def create_user(self, nickname: str, password_static: str, email: str) -> tuple[str, float, str, str]:
        password = helper.encryption(password_static)
        verify_code_for_nickname = auth_verify.generate_verify_code(nickname)

        try:
            if not helper.valid_email(email): raise VaildEmailError()

            reg_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            reg_f = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            self.supabase.table("Users").insert({
                "nickname": nickname,
                "password": password, 
                "play_time": 0.0,
                "register_time": reg_time,
                "verify_code": verify_code_for_nickname,
                "email": email
            }).execute()

            with open(os.path.join(build.config_folder, 'nicknames.json'), "r", encoding="ansi") as file:
                data = json.load(file)

            with open(os.path.join(build.config_folder, 'nicknames.json'), "w", encoding="ansi") as file:
                data["verify_code"][nickname] = verify_code_for_nickname
                data["nicknames"].append(nickname)
                data["last_nickname"] = nickname
                json.dump(data, file, indent=4, ensure_ascii=False)

            return (nickname, 0.0, reg_f, email)
        except Exception as e:
            if "duplicate key value violates unique constraint" in str(e): raise UserAlreadyExistsError()
            else: raise e

    def list_nicknames(self) -> list:
        try:
            with open(os.path.join(build.config_folder, 'nicknames.json'), "r", encoding="ansi") as file:
                data = json.load(file)
                
            nicknames = data["nicknames"]
            return_list = []

            response = self.supabase.table("Users").select("*").in_("nickname", nicknames).execute().data
            users_dict = {user['nickname']: user for user in response} # type: ignore
            sorted_users = [users_dict[name] for name in nicknames if name in users_dict]

            for user, nickname in zip(sorted_users, nicknames):
                time_play = user['play_time'] # type: ignore
                verify_code_db = user['verify_code'] # type: ignore
                verify_code = data["verify_code"][nickname]
                if verify_code == verify_code_db:
                    return_list += [[nickname, True, time_play]]
                else:
                    return_list += [[nickname, False, time_play]]

            return return_list
        except Exception as e:
            raise e
        
    def auth_in_account(self, nickname: str, password_static: str) -> tuple[str, float, str, str | None]:
        try:
            verify_code_for_nickname = auth_verify.generate_verify_code(nickname)
            password = helper.encryption(password_static)

            with open(os.path.join(build.config_folder, 'nicknames.json'), "r", encoding="ansi") as file:
                data = json.load(file)

            if nickname in data["nicknames"]: raise UserAlreadyAddedError()
            try: user_from_database = self.supabase.table("Users").select("*").eq("nickname", nickname).execute()
            except Exception as e: raise DataBaseError(e)

            if user_from_database.data == []: raise UserNotFoundError()

            if password == user_from_database.data[0]['password']: #type: ignore
                if user_from_database.data[0]["verify_code"] != verify_code_for_nickname: #type: ignore
                    try:
                        self.supabase.table("Users").update({"verify_code": verify_code_for_nickname}).eq("nickname", nickname).execute()
                    except Exception as e:
                        raise DataBaseError(e)
                    
                with open(os.path.join(build.config_folder, 'nicknames.json'), "w", encoding="ansi") as file:
                    data["verify_code"][nickname] = verify_code_for_nickname
                    data["nicknames"].append(nickname)
                    data["last_nickname"] = nickname
                    json.dump(data, file, indent=4, ensure_ascii=False)

                return (user_from_database.data[0]["nickname"], user_from_database.data[0]["play_time"], user_from_database.data[0]["register_time"], user_from_database.data[0]["email"]) #type: ignore
            else:
                raise NotCorrectPasswordError()
        except Exception as e:
            raise e

    def auth_in_account_retry(self, nickname: str, password_static: str) -> tuple[str, float, str, str | None]:
        try:
            verify_code_for_nickname = auth_verify.generate_verify_code(nickname)
            password = helper.encryption(password_static)

            with open(os.path.join(build.config_folder, 'nicknames.json'), "r", encoding="ansi") as file:
                data = json.load(file)

            try: user_from_database = self.supabase.table("Users").select("*").eq("nickname", nickname).execute()
            except Exception as e: raise e

            if user_from_database.data == []:raise UserNotFoundError()

            if password == user_from_database.data[0]['password']: #type: ignore
                try:
                    self.supabase.table("Users").update({"verify_code": verify_code_for_nickname}).eq("nickname", nickname).execute()
                except Exception as e:
                    raise DataBaseError(e)
                
                with open(os.path.join(build.config_folder, 'nicknames.json'), "w", encoding="ansi") as file:
                    data["verify_code"][nickname] = verify_code_for_nickname
                    data["last_nickname"] = nickname
                    json.dump(data, file, indent=4, ensure_ascii=False)

                return (user_from_database.data[0]["nickname"], user_from_database.data[0]["play_time"], user_from_database.data[0]["register_time"], user_from_database.data[0]["email"]) #type: ignore
            else:
                raise NotCorrectPasswordError()
        except Exception as e:
            raise e
        
    def exit_with_account(self, nickname: str) -> None:
        try:
            with open(os.path.join(build.config_folder, 'nicknames.json'), "r", encoding="ansi") as file:
                data = json.load(file)

            with open(os.path.join(build.config_folder, 'nicknames.json'), "w", encoding="ansi") as file_w:
                data["verify_code"][nickname] = "log in again"
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            raise e
        
    def update_play_time(self, nickname: str, play_time_plus: float) -> float:
        try:
            current_time = float(self.supabase.table("Users").select("play_time").eq("nickname", nickname).execute().data[0]['play_time']) #type: ignore
            self.supabase.table("Users").update({"play_time": current_time+play_time_plus}).eq("nickname", nickname).execute()
        except Exception as e:
            raise DataBaseError(e)
        return current_time + play_time_plus
    
    def retry_update_time(self) -> None:
        time_fixed = os.path.join(build.config_folder, "time_fixed.json")

        if os.path.isfile(time_fixed):
            try:
                with open(time_fixed, "r", encoding="ansi") as file: data = json.load(file)
                for nickname in list(data.keys()):
                    if data[nickname][1] != helper.encryption(data[nickname][0]): continue

                    play_time_plus = data[nickname][0]
                    current_time = float(self.supabase.table("Users").select("play_time").eq("nickname", nickname).execute().data[0]['play_time']) #type: ignore
                    self.supabase.table("Users").update({"play_time": current_time+play_time_plus}).eq("nickname", nickname).execute()
                    del data[nickname]
                with open(time_fixed, "w", encoding="ansi") as file: 
                    json.dump(data, file, indent=4, ensure_ascii=False)
                if len(data) == 0: os.remove(time_fixed)
            except Exception as e:
                raise e
            
    def select_data_user(self, nickname: str) -> tuple[str, float, str, str | None]:
        try:
            user_from_database = self.supabase.table("Users").select("*").eq("nickname", nickname).execute()
        except Exception as e:
            raise DataBaseError(e)
        return (user_from_database.data[0]["nickname"], user_from_database.data[0]["play_time"], user_from_database.data[0]["register_time"], user_from_database.data[0]["email"]) #type: ignore
    
    def download_mods_from_supabase(self, filename: str, path: pathlib.Path | str) -> int | None:
        try:
            response = (
                self.supabase.storage
                .from_("mods")
                .download(filename)
            )
            if len(response) != 0:
                with open(path, "wb") as f:
                    f.write(response)
        except Exception as e:
            if 'Object not found' in str(e): return 404
            else: raise e

auth_manager = AuthManager()