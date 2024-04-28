from utils.internal_interfaces import __times_password_been_leaked, __times_hash_been_leaked

def times_password_been_leaked(passwd: str):
    data = __times_password_been_leaked(passwd)

    return {
        "title" : f"The number of times the password {passwd} has been leaked",
        "xdata" : data
    }

def times_hash_been_leaked(passwd_hash: str):
    data = __times_hash_been_leaked(passwd_hash)

    return {
        "title" : f"The number of times the hash {passwd_hash} has been leaked",
        "xdata" : data
    }