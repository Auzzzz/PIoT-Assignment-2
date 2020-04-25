import os
import hashlib

salt = os.urandom(32)
password = 'password123'

key = hashlib.pbkdf2_hmac(
    'sha256', #Hash digest for HMC
    password.encode('utf-8'), #Convert the password to bytes
    salt, #Provide the salt
    100000 #Number of iterations of SHA-256, 100000 is recommended
)

#Password check
pass_to_check = 'password123'

new_key = hashlib.pbkdf2_hmac(
    'sha256',
    pass_to_check.encode('utf-8'),
    salt,
    100000
)

if new_key == key:
    print("Password is correct")
else:
    print("Password is incorrect")

class Hash:
    def hash(self):
        