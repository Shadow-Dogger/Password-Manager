import tkinter as tk
from Crypto.Cipher import AES as crypto
import hashlib as hashlib
import json as json
import pathlib as pathlib
import ast as ast
window = tk.Tk()
master_key = ""

class AccountStorage:
    """
    Problems:
        1. Encrypt password
        2. Store Password with username and stie
        3. Retrieve encrypted password
        4. decrypt encrypted password
        5. bundle the decrypted password, site and username together



    Solutions
        1. AES_SIV allows for deterministic hashes
        2. Write site, username, and password into a text file as a json object(doing so allows me to keep all the information bundled as a dictionary which is neat with the site as a key)
        3. read the file as a json object
        4. Parse the json object into its 3 seperate parts, then run the encrypted password through the decryption function
        5. break down the json object
    """

    def __init__(self, site: str, username: str, password=""):
        self.site = site
        self.username = username
        self.password = password.encode()
        self.key = master_key
        self.tag =""

    def key_management(self):
        key_amplifier = hashlib.sha256()
        key_amplifier.update(self.key.encode())
        self.key = key_amplifier.hexdigest().encode()

    def pass_encryption(self):
        cipher = crypto.new(self.key, crypto.MODE_SIV, nonce=None)

        cipher.update(b'header')
        print(type(self.password))
        ciphertext, self.tag = cipher.encrypt_and_digest(self.password)
        print(ciphertext)
        with open(str(pathlib.Path(__file__).parent.resolve()) + "\\Passwords", "a") as pass_write:
            pass_write.write(json.dumps({self.site: {self.username: str(ciphertext)}})+"\n")
        return ciphertext

    def pass_decryption(self, look_site):
        with open(str(pathlib.Path(__file__).parent.resolve()) + "\\Passwords", 'r') as file:
            for i in file.readlines():
                if look_site in i:
                    print(type(i))
                    print(i)
                    res = json.loads(i)
                    print(type(res))

                    log = list(res.keys())
                    cipher = crypto.new(self.key, crypto.MODE_SIV, nonce=None)
                    cipher.update(b'header')
                    user = list(res[log[0]].keys())[0]
                    password=res[log[0]][user]
                    
                    
                    
                    return {log[0]:{user:cipher.decrypt_and_verify(ast.literal_eval(password),self.tag)}}

        

