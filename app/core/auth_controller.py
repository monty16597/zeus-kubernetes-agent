import jwt
from .db import check_user_in_db
from fastapi import HTTPException, Depends
from .config import (
    JWT_KEY, JWT_ALGORITHM, JWT_TOKEN_TYPE, JWT_TOKEN_EXPIRY, OAUTH_SCHEME)


def encode_jwt_token(payload):
    return {
        'access_token': jwt.encode({'exp': JWT_TOKEN_EXPIRY,
                                    'username': payload.username,
                                    'token_type': JWT_TOKEN_TYPE,
                                    'password': payload.password},
                                   JWT_KEY, algorithm=JWT_ALGORITHM)
    }


async def decode_jwt_token(token: str = Depends(OAUTH_SCHEME)):
    """
    description: This function will decode the JWT token and check the authentication using token.

    param: token: the Authorization token from the incoming requests.
    """
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
        if not check_user_in_db(payload.get('username'), payload.get('password')):
            raise HTTPException(status_code=403, detail='Token is not valid')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail='Token is expired')
