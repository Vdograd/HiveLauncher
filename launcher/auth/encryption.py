import hashlib

def encryption_password(password):
    password_hash = hashlib.sha256()
    password_hash.update(password.encode('utf-8'))
    return password_hash.hexdigest()
