import unittest
from cherry_jwt.jwt import JWT
from cherry_jwt.verifier import JWTVerifier
from cherry_jwt.exceptions import JWTEncodeException, JWTVerificationException

class TestHS256(unittest.TestCase):
    def test_set_header_works(self):
        jwt = JWT({}, "HS256", "secret")
        jwt = jwt.set_header_val("FOO", "BAR")
        self.assertEqual(jwt.header["FOO"], "BAR")

    def test_allow_none_algorithm(self):
        jwt = JWT({}, "none", "secret")
        jwt = jwt.allow_none_value_for_algorithm()
        jwt.encode()

    def test_non_explicit_none_algorithm_fails(self):
        jwt = JWT({"message": "hello world"}, "none", "secret")
        self.assertRaises(JWTEncodeException, jwt.encode)

    def test_setting_typ_helper_works(self):
        jwt = JWT({}, "HS256", "secret")
        jwt = jwt.typ("JWT--X")
        self.assertEqual(jwt.header["typ"], "JWT--X")
    
    def test_iss_convenience_checking_method_works(self):
        jwt = JWT({"iss": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_iss_is("xxx")
        jwt_verifier.verify(jwt)

        jwt = JWT({"iss": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_iss_is("yyy")
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)
    
    def test_sub_convenience_checking_method_works(self):
        jwt = JWT({"sub": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_sub_is("xxx")
        jwt_verifier.verify(jwt)

        jwt = JWT({"sub": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_sub_is("yyy")
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)
    
    def test_jti_convenience_checking_method_works(self):
        jwt = JWT({"jti": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_jti_is("xxx")
        jwt_verifier.verify(jwt)

        jwt = JWT({"jti": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_jti_is("yyy")
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)
    
    def test_nbf_convenience_checking_method_works(self):
        jwt = JWT({"nbf": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_nbf_is("xxx")
        jwt_verifier.verify(jwt)

        jwt = JWT({"nbf": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_nbf_is("yyy")
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)
    
    def test_iat_convenience_checking_method_works(self):
        jwt = JWT({"iat": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_iat_is("xxx")
        jwt_verifier.verify(jwt)

        jwt = JWT({"iat": "xxx"}, "HS256", b"secret").encode()
        jwt_verifier = JWTVerifier("HS256", b"secret").check_iat_is("yyy")
        self.assertRaises(JWTVerificationException, jwt_verifier.verify, jwt)


if __name__ == "__main__":
    unittest.main()
