import bcrypt


def encode_password(password):
    if isinstance(password, str):
        return bcrypt.hashpw(password, bcrypt.gensalt(prefix=b"2a"))
