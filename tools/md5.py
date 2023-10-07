import hashlib
import base64


def to_md5(bin):
    result = hashlib.md5(bin)
    encoded = base64.b64encode(result.digest())
    return encoded.decode("ascii")

