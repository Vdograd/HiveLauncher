import socket
import hashlib

class AuthVerify:
    def generate_verify_code(self, nickname):
        nickname = str(nickname)
        hostname = str(socket.gethostname())
        str_verify = nickname + hostname
        sha256_code = hashlib.sha256()
        sha256_code.update(str_verify.encode('utf-8'))
        code_sha256 = sha256_code.hexdigest()
        return str(code_sha256)