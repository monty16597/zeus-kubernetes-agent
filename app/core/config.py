import os
from kubernetes import config
from fastapi.security import OAuth2PasswordBearer
from .utils import get_jwt_expiry_time

# Configs can be set in Configuration class directly or using helper utility
if os.environ.get('APP_ENV') == 'production':
    config.load_incluster_config()
else:
    config.load_kube_config()

JWT_KEY = os.environ.get('APP_JWT_KEY', 'cLSYLkHwQcznat89JcgWTwqM6innaUufHmLVjAf4EQT9FDQVnsz6LkBtjo78GUQP')
JWT_ALGORITHM = os.environ.get('APP_JWT_ALGO', 'HS256')
JWT_TOKEN_TYPE = os.environ.get('JWT_TOKEN_TYPE', 'bearer')
JWT_TOKEN_EXPIRY = get_jwt_expiry_time(hours=1)

OAUTH_SCHEME = OAuth2PasswordBearer(tokenUrl='token')
