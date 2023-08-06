import base64
import json

from cherry_jwt.crypto import (deserialize_private_key, ecdsa_sign,
                    hmac_sha_256_generate_mac)
from cherry_jwt.exceptions import JWTEncodeException
from cherry_jwt.util import check_is_valid_algorithm


class JWT:
    def __init__(
        self, claims: dict[str, str], algorithm: str, secret: any, format=None
    ) -> None:
        self.claims = claims
        self.algorithm = algorithm.upper()
        self.secret = secret
        self.header = {"alg": self.algorithm, "typ": "JWT"}
        self.none_for_algorithm_allowed = False
        if not format and algorithm == "ECDSA":
            raise JWTEncodeException("No format was provided for ECDSA private key")
        elif algorithm == "ECDSA" and format not in {"PEM", "DER"}:
            raise JWTEncodeException(
                "ECDSA private key needs to be in PEM or DER format"
            )
        self.format = format
        check_is_valid_algorithm(self.algorithm)

    def allow_none_value_for_algorithm(self):
        self.none_for_algorithm_allowed = True
        return self

    def typ(self, typ):
        self.header["typ"] = typ
        return self

    def set_header_val(self, key: str, val: str):
        self.header[key] = val
        return self

    def _sign(self, header_encoded: bytes, claims_encoded: bytes) -> str:
        signature_or_mac_function = {
            "HS256": hmac_sha_256_generate_mac,
            "ECDSA": ecdsa_sign,
            "NONE": lambda x, y, z: b"",
        }[self.algorithm]
        if self.algorithm == "ECDSA":
            self.secret = deserialize_private_key(self.format, self.secret)
        return signature_or_mac_function(header_encoded, claims_encoded, self.secret)

    def encode(self):
        if self.algorithm == "NONE" and not self.none_for_algorithm_allowed:
            raise JWTEncodeException("None algorithm not allowed")

        header_encoded = base64.urlsafe_b64encode(
            bytes(json.dumps(self.header), "utf-8")
        ).rstrip(b"=")

        claims_encoded = base64.urlsafe_b64encode(
            bytes(json.dumps(self.claims), "utf-8")
        ).rstrip(b"=")

        signature_or_mac = self._sign(header_encoded, claims_encoded)
        return header_encoded + b"." + claims_encoded + b"." + signature_or_mac
