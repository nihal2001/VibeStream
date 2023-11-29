import hashlib

def hash(password):
    print(hashlib.sha256(password.encode()).hexdigest())

hash("password")