from hashlib import sha256

from django.conf import settings

def sha256_code(strings):
    key = settings.SECRET_KEY
    has256 = sha256()
    has256.update((strings + key).encode('utf-8'))
    pwd = has256.hexdigest()
    return pwd[:30]