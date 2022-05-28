import base64, hashlib, os, subprocess, tempfile, sys
from Crypto.Cipher import AES

class Anubis:

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key).digest()

    def decrypt(self, enc):
        enc = base64.b64decode(str(enc))
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def load(file):
    with open(file, "r") as f:
        obfcode = f.read()
    obfcode = obfcode.replace("import ancrypt\nancrypt.load(__file__)\n'''", "").replace("\n'''", "")
    listed = obfcode.split("__ANUBIS_ENCRYPTED__" * 25)
    del listed[0]; del listed[-1]
    key = listed[0].encode()
    del listed[0]
    anubis = Anubis(key)
    src = ""
    for i in listed:
        src += anubis.decrypt(i) + "\n"
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.write(src.encode())
    p = subprocess.Popen([sys.executable, tmp.name])
    tmp.close()
    p.wait()
    os.unlink(tmp.name)