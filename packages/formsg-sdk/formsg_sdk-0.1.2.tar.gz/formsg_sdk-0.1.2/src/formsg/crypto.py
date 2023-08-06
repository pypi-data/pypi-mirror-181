import base64
import json
import time

from nacl.public import PrivateKey, PublicKey,Box
from nacl.encoding import Base64Encoder
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

def decrypt_content(formsecretkey: str, encryptedContent: str):
    formpublickey, data = encryptedContent.split(';')

    #FormSG encodes keys in B64. To supply the keys in correct format, we have to specify the encoding.
    box = Box(PrivateKey(formsecretkey,Base64Encoder), PublicKey(formpublickey,Base64Encoder))
    plaintext = box.decrypt(base64.b64decode(data)).decode('utf-8')

    return json.loads(plaintext)

#FormSG sends 't' in milliseconds(ms). time.time() in python returns in seconds(s).
#FormSG uses a tolerance of 5 mins to prevent replay attacks.
def has_epoch_expired(epoch: float, expiry = 300000):
    return abs(time.time()*1000 - epoch) > expiry


def verify_sig_headers(request_uri: str, formsg_sig_header: str):
    formsg_publickey = '3Tt8VduXsjjd4IrpdCd7BAkdZl/vUCstu9UvTX84FWw='
    verifykey = VerifyKey(formsg_publickey, encoder = Base64Encoder)
    
    #Documentation for manual verification: 
    #https://github.com/opengovsg/formsg-javascript-sdk#verifying-signatures-manually
    sig_dict = {}
    for item in formsg_sig_header.split(','):
        k, v = item.split('=',1)
        sig_dict[k] = v

    if has_epoch_expired(float(sig_dict['t'])):
        raise BadSignatureError(f'FormSG signature is not recent. Epoch={sig_dict["t"]}, now={str(time.time()*1000)}')

    base_string = '.'.join([request_uri, sig_dict['s'], sig_dict['f'], sig_dict['t']])
    verifykey.verify(smessage = base_string.encode('ascii'), signature = Base64Encoder.decode(sig_dict['v1']))

    return
