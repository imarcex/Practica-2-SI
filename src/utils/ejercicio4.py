from utils.internal_interfaces import __times_password_been_leaked, __times_hash_been_leaked

def times_password_been_leaked(passwd: str):
    return __times_password_been_leaked(passwd)

def times_hash_been_leaked(passwd_hash: str):
    return __times_hash_been_leaked(passwd_hash)
