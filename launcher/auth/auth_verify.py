from ..utils.helper import helper
import socket

class AuthVerify:
    def generate_verify_code(self, nickname: str) -> str:
        hostname = socket.gethostname()
        str_verify = nickname + hostname
        return helper.encryption(str_verify)
    
auth_verify = AuthVerify()