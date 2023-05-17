import hashlib
import base64


def to_md5(bin):
    result = hashlib.md5(bin)
    encoded = base64.b64encode(result.digest())
    return encoded.decode("ascii")


#file = open("../zelda1.nes", "rb")
#print(to_md5(file.read()))