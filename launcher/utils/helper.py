import psutil
import re
import os
from screeninfo import get_monitors
import subprocess
import traceback
import hashlib

class Helper:
    def get_rem(self, rem):
        virtual_memory = psutil.virtual_memory()
        total_gb = virtual_memory.total / (1024 ** 3)
        total_mb = virtual_memory.total / (1024 ** 2)
        if rem == "mb":
            return total_mb
        elif rem == "gb":
            return round(total_gb)
        
    def access_rem(self):
        rem_list = ["0.5"]
        for x in range(1, 257):
            rem_list.append(str(x))
        rem = self.get_rem("gb")
        rem_list_out = []
        for x in rem_list:
            if float(x) < float(rem):
                rem_list_out.append(x + f" GB - {int(float(x)*1024)} MB")
        return rem_list_out
    
    def screen(self):
        a = get_monitors()[0]
        return (a.width, a.height)

    def access_screens(self):
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
    
    def default_rem(self): 
        rem = self.access_rem()
        if len(rem) > 3:
            rem = rem[2]
        else:
            rem = rem[0]
        return rem
    
    def find_pattern(self, num1, pattern):
        escaped_pattern = re.escape(pattern)
        regex_pattern = f"(?<![\\d.]){escaped_pattern}(?![\\d.])"
        
        if re.search(regex_pattern, num1):
            return num1
        else:
            return None

    def find_versions_folders(self, path: str):
        items = os.listdir(path)
        folders = [item for item in items if os.path.isdir(os.path.join(path, item))]
        return folders
    
    def get_java(self):
        try:
            result = subprocess.run(['java', '-version'], capture_output=True, text=True, check=False)
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
    
    def get_traceback(self, e):
        new = []
        af = traceback.format_exc().split("\n")
        for x in af:
            new.append(f"|   {x}")
        return new
    
    def hash_time_add(self, plustime):
        time = str(plustime)
        hash256 = hashlib.sha256()
        hash256.update(time.encode('utf-8'))
        return hash256.hexdigest()