import random
from django.conf import settings
from django.utils.encoding import smart_str
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
from Paymenypayfort.settings import PASSWORD_ENCRYPTION


def get_hexdigest(algorithm, salt, raw_password):
    """
    Returns a string of the hexdigest of the given plaintext password and salt
    using the given algorithm ('md5', 'sha1' or 'crypt').
    """
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        md5 = hashlib.md5()
        return md5.update(salt + raw_password).digest()
    elif algorithm == 'sha1':
        return hashlib.sha1((salt + raw_password).encode('utf-8')).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def set_password(password, algo=PASSWORD_ENCRYPTION):
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, password)
    return '%s$%s$%s' % (algo, salt, hsh)


def check_password(user_password, password, algo=PASSWORD_ENCRYPTION):
    salt = user_password.split('$')[1]
    hsh = get_hexdigest(algo, salt, password)
    return '%s$%s$%s' % (algo, salt, hsh)


# def get_user_password(username, algo=PASSWORD_ENCRYPTION):
#     if '@' in username:
#         kwargs = {'email': username}
#     else:
#         kwargs = {'phone_number': username}
#
#     user = Users.objects.get(**kwargs)
#     user_passwd = user.password
#     salt = user_passwd.split('$')[1]
#     hsh = get_hexdigest(algo, salt, user_passwd)
#     return '%s$%s$%s' % (algo, salt, hsh)