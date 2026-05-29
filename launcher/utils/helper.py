import hashlib
import os

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
    
helper = Helper()