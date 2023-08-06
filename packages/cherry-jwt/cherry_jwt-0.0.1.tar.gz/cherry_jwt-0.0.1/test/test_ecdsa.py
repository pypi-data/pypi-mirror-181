import unittest
from cherry_jwt.jwt import JWT
from cherry_jwt.verifier import JWTVerifier
from cherry_jwt.exceptions import JWTVerificationException
from ellipticcurve import PrivateKey


class TestECDSA(unittest.TestCase):
    def test_ecdsa_empty_jwt_pem_format(self):
        private_key = PrivateKey()
        private_key_pem, public_key_pem = (
            private_key.toPem(),
            private_key.publicKey().toPem(),
        )
        jwt = JWT({}, "ECDSA", bytes(private_key_pem, "utf-8"), format="PEM").encode()
        jwt_verifier = JWTVerifier(
            "ECDSA", bytes(public_key_pem, "utf-8"), {}, format="PEM"
        )
        jwt_verifier.verify(jwt)

    def test_ecdsa_empty_jwt_der_format(self):
        private_key = PrivateKey()
        private_key_der, public_key_der = (
            private_key.toDer(),
            private_key.publicKey().toDer(),
        )
        jwt = JWT({}, "ECDSA", private_key_der, format="DER").encode()
        jwt_verifier = JWTVerifier("ECDSA", public_key_der, {}, format="DER")
        jwt_verifier.verify(jwt)

    def test_bad_ket_ecdsa_empty_jwt_pem_format(self):
        private_key = PrivateKey()
        private_key_pem, bad_public_key_pem = (
            private_key.toPem(),
            PrivateKey().publicKey().toPem(),
        )
        jwt = JWT({}, "ECDSA", bytes(private_key_pem, "utf-8"), format="PEM").encode()
        jwt_verifier = JWTVerifier(
            "ECDSA", bytes(bad_public_key_pem, "utf-8"), {}, format="PEM"
        )
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)

    def test_bad_key_ecdsa_empty_jwt_der_format(self):
        private_key = PrivateKey()
        private_key_der, bad_public_key_der = (
            private_key.toDer(),
            PrivateKey().publicKey().toDer(),
        )
        jwt = JWT({}, "ECDSA", private_key_der, format="DER").encode()
        jwt_verifier = JWTVerifier("ECDSA", bad_public_key_der, {}, format="DER")
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)


if __name__ == "__main__":
    unittest.main()
