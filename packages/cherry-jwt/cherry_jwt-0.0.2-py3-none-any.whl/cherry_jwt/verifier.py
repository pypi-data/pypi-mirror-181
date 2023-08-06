import base64
import datetime
import json

from cherry_jwt.crypto import (deserialize_public_key, ecdsa_verify,
                    hmac_sha_256_verify_mac)
from cherry_jwt.exceptions import JWTVerificationException
from cherry_jwt.util import check_is_valid_algorithm


class JWTVerifier:
    def __init__(
        self,
        algorithm: str,
        key: str | bytes,
        claims_validator: dict[str, str] | None = None,
        format=None,
    ) -> None:
        self.algorithm = algorithm.upper()
        self.key = key
        self.claims_validator = claims_validator if claims_validator else {}
        self.expired_now_check = False
        self.throw_exception_on_failure = False
        if not format and algorithm == "ECDSA":
            raise JWTVerificationException(
                "No format was provided for ECDSA public key"
            )
        elif algorithm == "ECDSA" and format not in {"PEM", "DER"}:
            raise JWTVerificationException(
                "ECDSA public key needs to be in PEM or DER format"
            )
        self.format = format
        check_is_valid_algorithm(self.algorithm)

    def throw_exception_on_verification_failure(self):
        self.throw_exception_on_failure = True

    def check_iss_is(self, val: str):
        self.claims_validator["iss"] = val
        return self

    def check_aud_is(self, val: str):
        self.claims_validator["aud"] = val
        return self

    def check_sub_is(self, val: str):
        self.claims_validator["sub"] = val
        return self

    def check_exp_is(self, val: str):
        if self.expired_now_check:
            raise JWTVerificationException("Exp check must be hardcoded or default.")
        self.claims_validator["exp"] = val
        return self

    def check_nbf_is(self, val: str):
        self.claims_validator["nbf"] = val
        return self

    def check_iat_is(self, val: str):
        self.claims_validator["iat"] = val
        return self

    def check_jti_is(self, val: str):
        self.claims_validator["jti"] = val
        return self

    def check_exp_against_current_times(self):
        if self.claims_validator.get("exp"):
            raise JWTVerificationException("Exp check must be hardcoded or default.")
        self.expired_now_check = True

    def _decode(self, urlsafeb64: bytes):
        return json.loads(base64.urlsafe_b64decode(urlsafeb64 + (b"=")))

    def verify(self, jwt: bytes):
        try:
            header_encoded, claims_encoded, signature_or_mac = jwt.split(b".")
        except ValueError:
            raise JWTVerificationException("JWT is badly formatted, can not decode it.")

        header, claims = self._decode(header_encoded), self._decode(claims_encoded)
        if not header.get("alg") or header["alg"] != self.algorithm:
            raise JWTVerificationException(
                "Could not find algorithm in decoded header."
            )

        verification_function = {
            "HS256": hmac_sha_256_verify_mac,
            "ECDSA": ecdsa_verify,
            "NONE": lambda a, b, c, d: True
        }[self.algorithm]

        if self.algorithm == "ECDSA":
            self.key = deserialize_public_key(self.format, self.key)
        if not verification_function(
            header_encoded, claims_encoded, signature_or_mac, self.key
        ):
            raise JWTVerificationException(
                f'Verification of the {"mac" if self.algorithm == "HS256" else "signature"} failed.'
            )

        for claim in self.claims_validator:
            if not claims.get(claim):
                raise JWTVerificationException(
                    f"Did not find claim {claim} in decoded JWT."
                )

            if self.check_exp_against_current_times and claim == "exp":
                time_of_exp = datetime.datetime.fromtimestamp(claims[claim])
                if not time_of_exp > datetime.datetime.now():
                    raise JWTVerificationException("JWT is expired.")

            elif self.claims_validator[claim] != claims[claim]:
                raise JWTVerificationException(
                    f"Expect claim {claim} to have value {self.claims_validator[claim]} not {claims[claim]}"
                )
