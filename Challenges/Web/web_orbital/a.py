import os, hashlib, jwt, datetime
from flask import jsonify,abort,session
from functools import wraps

def passwordVerify(hashPassword, password):
    md5Hash = hashlib.md5(password.encode())

    if md5Hash.hexdigest() == hashPassword: return True
    else: return False

# function genPass() {
#     echo -n 'ichliebedich' | md5sum | head -c 32
# }
# print(genPass())  # Example usage, should print the MD5 hash of 'ichliebedich'

print(hashlib.md5('ichliebedich'.encode()).hexdigest())  # Example usage, should print the MD5 hash of 'ichliebedich'

print(passwordVerify('5f4dcc3b5aa765d61d8327deb882cf99', 'password'))  # Example usage, should return True