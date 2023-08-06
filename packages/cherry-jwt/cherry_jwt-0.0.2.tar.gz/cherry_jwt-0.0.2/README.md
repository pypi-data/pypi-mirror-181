# Cherry JWT
**Warning**
<br/>
An simple implementation of JWT for educational purposes.
<br/>
Please do not use this in a real application.

# Installation
``pip install cryptography starkbank-ecdsa cherry_jwt``

# Usage

## Creating a JWT with HS256 (mac)
``` python
from cherry_jwt.jwt import JWT

jwt = JWT(
    claims={
        'message': 'hello world'
    }, 
    algorithm='HS256', 
    secret='secret'
).encode()
```

## Verifying a JWT with HS256
``` python
from cherry_jwt.verifier import JWTVerifier
from cherry_jwt.exceptions import JWTVerificationException

jwt_verifier = JWTVerifier(algorithm='HS256', key='secret', claims_validator={
    'message': 'hello world'
})

try:
    jwt_verifier.verify(jwt)
except JWTVerificationException as e:
    #handle rejection
    print(e)
```

## Creating a JWT with ECDSA

``` python
from cherry_jwt.jwt import JWT

 #can accept key as PEM or DER
private_key_pem = get_private_key_pem()
jwt = JWT(
    claims={
        'message': 'hello world'
    }, 
    algorithm='ECDSA', 
    secret=private_key_pem,
    format='PEM'
).encode()
```

## Verifying a JWT with ECDSA

``` python
from cherry_jwt.verifier import JWTVerifier
from cherry_jwt.exceptions import JWTVerificationException

jwt_verifier = JWTVerifier(
    algorithm='ECDSA', 
    key=public_key_pem, 
    claims_validator={
        'message': 'hello world'
    }),
    format='PEM'

try:
    jwt_verifier.verify(jwt)
except JWTVerificationException as e:
    #handle rejection
    print(e)
```

## Set header
```python
jwt = JWT(
    claims={
        'message': 'hello world'
    }, 
    algorithm='HS256', 
    secret='secret'
).set_header_val('FOO', 'BAR').encode()
```

## Convenience methods for common claims
```python
jwt_verifier = JWTVerifier(algorithm='HS256', key='secret', claims_validator={
    'message': 'hello world'
}).check_aud_is('xxx').check_iss_is('yyy').check_sub_is('zzz')
```


