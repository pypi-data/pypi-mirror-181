import unittest
from cherry_jwt.jwt import JWT
from cherry_jwt.verifier import JWTVerifier
from cherry_jwt.exceptions import JWTVerificationException


class TestHS256(unittest.TestCase):
    def test_hs256_works_empty_jwt(self):
        jwt = JWT({}, "HS256", "secret").encode()
        jwt_verifier = JWTVerifier("HS256", "secret", {})
        jwt_verifier.verify(jwt)

    def test_hs256_reject_bad_mac_empty_jwt(self):
        jwt = JWT({}, "HS256", "secret").encode()
        jwt_verifier = JWTVerifier("HS256", "wrong_secret!!!", {})
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)

    def test_hs256_reject_bad_claims(self):
        jwt = JWT({"message": "hello world"}, "HS256", "secret").encode()
        jwt_verifier = JWTVerifier("HS256", "secret", {"message": "Wrong message"})
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)



if __name__ == "__main__":
    unittest.main()
