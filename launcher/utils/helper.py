from screeninfo import get_monitors
import subprocess
import traceback
import hashlib
import psutil
import os
import re

class Helper:
    def get_path_project(self, type_start: int) -> str:
        internal = os.path.join(os.path.dirname(os.path.abspath("main.py")), '_internal')
        default = os.path.join(os.path.dirname(os.path.abspath("main.py")))
        if type_start == 0:
            if os.path.exists(internal): return internal
            else: raise FileNotFoundError("Internal directory not found.")
        elif type_start == 1:
            if os.path.exists(default): return default
            else: raise FileNotFoundError("Default directory not found.")
        else:
            raise ValueError("Invalid type_start value. Must be 0 or 1.")
        
    def hash_time_add(self, plustime: float) -> str:
        time = str(plustime)
        hash256 = hashlib.sha256()
        hash256.update(time.encode('utf-8'))
        return hash256.hexdigest()
    
    def get_traceback(self, e: Exception) -> list:
        message = f"{e}" if f"{e}" != '' else 'None data error'
        new = []
        list_lines = traceback.format_exc().split("\n")
        for x in list_lines:
            if 'NoneType: None' == x:
                x = message
            new.append(f"|   {x}")
        return new
    
    def get_java(self) -> str | None:
        try:
            result = subprocess.run(
                ['java', '-version'], 
                capture_output=True, 
                text=True, 
                check=False, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            version_output = result.stderr if result.stderr else result.stdout
            match = re.search(r'version "([^"]+)"', version_output)
            if match:
                return match.group(1)
            
            match = re.search(r'(\d+\.\d+\.\d+[_\d]*)', version_output)
            if match:
                return match.group(1)
            return None
        except FileNotFoundError:
            return None
        except Exception:
            return 'Error'
    
    def get_rem(self, rem: str) -> int | float:
        virtual_memory = psutil.virtual_memory()
        total_gb = virtual_memory.total / (1024 ** 3)
        total_mb = virtual_memory.total / (1024 ** 2)
        if rem == "mb":
            return total_mb
        elif rem == "gb":
            return round(total_gb)
        else:
            raise TypeError('Invalid rem value. Must be "mg" or "gb".')

    def access_rem(self) -> list:
        rem_list = ["0.5"]
        for x in range(1, 257):
            rem_list.append(str(x))
        rem = self.get_rem("gb")
        rem_list_out = []
        for x in rem_list:
            if float(x) < float(rem):
                rem_list_out.append(x + f" GB - {int(float(x)*1024)} MB")
        return rem_list_out

    def default_rem(self) -> str: 
        rem = self.access_rem()
        if len(rem) > 3:
            rem = rem[2]
        else:
            rem = rem[0]
        return rem
    
    def screen(self) -> tuple[int, int]:
        a = get_monitors()[0]
        return (a.width, a.height)

    def access_screens(self) -> list:
        ren = []
        screens = [
            (925, 530),(640, 480), (800, 600),(1024, 768),(1152, 864),(1280, 720),(1280, 768),
            (1280, 800),(1280, 960),(1280, 1024),(1360, 768),(1366, 768),(1400, 1050),(1440, 900),
            (1600, 900),(1600, 1200),(1680, 1050),(1920, 1080),(1920, 1200),(2048, 1152),(2048, 1536),
            (2160, 1440),(2256, 1504),(2304, 1440),(2560, 1080),(2560, 1440),(2560, 1600),(2880, 1800),
            (3000, 2000),(3200, 1800),(3440, 1440),(3456, 2234),(3840, 1600),(3840, 2160),(4096, 2160),
            (4480, 2520), (5120, 1440),(5120, 2160),(5120, 2880),(6016, 3384),(7680, 4320),
        ]
        screen_home = self.screen()
        for scr in screens:
            if scr[0] <= screen_home[0] and scr[1] <= screen_home[1]:
                ren.append(f"{scr[0]}x{scr[1]}")
        return ren
    
helper = Helper()