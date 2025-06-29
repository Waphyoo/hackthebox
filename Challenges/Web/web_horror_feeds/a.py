import os, bcrypt, jwt, datetime
def generate_password_hash(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

a=generate_password_hash('admin2')
print(a)

def verify_hash(password, passhash):
    return bcrypt.checkpw(password.encode(), passhash.encode())

print(verify_hash('admin2', '$2b$12$Wv.6cHnG0BxuxZ82/oy2MeEgy2LG6C.O2n6Ig7GwNegw2zGB22dm2'))