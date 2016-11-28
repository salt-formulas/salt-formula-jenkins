import hashlib
import random
import string

def encode_password(password):
    salt = ''.join(random.SystemRandom().choice(string.ascii_letters)
                   for i in range(6))
    hash_ = hashlib.sha256("%s{%s}" % (password, salt)).hexdigest()
    return "%s:%s" % (salt, hash_)