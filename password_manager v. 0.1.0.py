import tkinter as tk
from Crypto.Cipher import AES as crypto
import hashlib as hashlib
import json as json
import pathlib as pathlib
import ast as ast
window = tk.Tk()
master_key = "twenty"


class AccountStorage:
    """
    
    Will contain all the entire practical coding of a password manager
    
    ask python discord about turning a string of a dictionary into a real dictionary, should solve all problems
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

        if i is None:
            return

'''
class Gui:
    

    def __init__():

        t.tk()






    def basic_layout():
        main_message = tk.Label(

            text="Shadow Dogger's Password Manager",
            height=5,
            width=30,
            foreground="white",
            background="black",

        )

        main_screen = tk.Label(

        background="white",
        height=10,
        width=100
    )

        main_message.pack()
        main_screen.pack()

window.mainloop()


'''
