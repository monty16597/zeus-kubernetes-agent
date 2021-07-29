from .auth_controller import encode_jwt_token
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["auth"],
)

@router.post("/token")
async def token_generator(form_data: OAuth2PasswordRequestForm = Depends()):
    return encode_jwt_token(form_data)