import pickle
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization



def generate_keys():
    private = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public = private.public_key()
    pu_ser = public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return private, pu_ser


def sign(message, private):
    message = bytes(str(message), "utf-8")
    sig = private.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig


def verify(message, sig, pu_ser):
    loaded_pu = serialization.load_pem_public_key(
        pu_ser,
    )
    message = bytes(str(message), "utf-8")
    try:
        loaded_pu.verify(
        sig,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
        return True
    except InvalidSignature:
        return False
    except:
        print("Error verifying public signature")



if __name__ == "__main__":
    pr, pu = generate_keys()
    message = b"This is my message"
    sig = sign(message, pr)
    correct = verify(message, sig, pu)

    if correct:
        print("success!")
    else:
        print("error, sig is invalid")

    pr2, pu2 = generate_keys()

    sig2 = sign(message, pr2)


    correct = verify(message, sig2, pu)

    if correct:
        print("ERROR, Bad signature works")
    else:
        print("Success, bad sig detected")

    badmess = messasge = b"Q"
    correct = verify(badmess, sig, pu)

    if correct:
        print("ERROR, Tampered message not detected")
    else:
        print("Success, tampered message detected")
