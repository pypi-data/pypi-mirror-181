import base64
import binascii
import hashlib
import hmac

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


def deserialize_private_key(format, data):
    deserialize_function = (
        serialization.load_pem_private_key
        if format == "PEM"
        else serialization.load_der_private_key
    )
    return deserialize_function(data, None)


def deserialize_public_key(format, data):
    deserialize_function = (
        serialization.load_pem_public_key
        if format == "PEM"
        else serialization.load_der_public_key
    )
    return deserialize_function(data)


def hmac_sha_256_generate_mac(
    header_encoded: bytes, claims_encoded: bytes, secret: str | bytes
) -> bytes:
    return base64.urlsafe_b64encode(
        hmac.new(
            key=bytes(secret, "utf-8") if type(secret) != bytes else secret,
            msg=header_encoded + b"." + claims_encoded,
            digestmod=hashlib.sha256,
        ).digest()
    ).rstrip(b"=")


def hmac_sha_256_verify_mac(
    header_encoded: bytes, claims_encoded: bytes, mac: bytes, secret: str | bytes
) -> bool:
    return (
        hmac_sha_256_generate_mac(header_encoded, claims_encoded, secret).rstrip(b"=")
        == mac
    )


def ecdsa_sign(header_encoded: bytes, claims_encoded: bytes, private_key: any) -> bytes:
    return base64.urlsafe_b64encode(
        private_key.sign(
            header_encoded + b"." + claims_encoded, ec.ECDSA(hashes.SHA256())
        )
    ).rstrip(b"=")


def ecdsa_verify(
    header_encoded: bytes, claims_encoded: bytes, signature: bytes, public_key: any
) -> bytes:
    try:
        signature = base64.urlsafe_b64decode(signature + b"=")
    except binascii.Error:
        signature = base64.urlsafe_b64decode(signature + b"==")
    try:
        public_key.verify(
            signature, header_encoded + b"." + claims_encoded, ec.ECDSA(hashes.SHA256())
        )
        return True
    except:
        return False
