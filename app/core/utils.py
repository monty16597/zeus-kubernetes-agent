from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import string
import random


def get_jwt_expiry_time(hours=0, minutes=0, seconds=0):
    """
    Description: generate shifted timestamp.
    return: datetime
    """
    if hours or minutes or seconds:
        return (
            datetime.utcnow() + timedelta(hours=hours, minutes=minutes, seconds=seconds))
    return datetime.utcnow() + timedelta(hours=100)


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_uppercase +
                                  string.digits, k=length))


def return_json_resp(status_code=200, message='Data', data=None):
    return JSONResponse(status_code=status_code, content={'message': message, 'data': jsonable_encoder(data)}) \
        if data else JSONResponse(status_code=404, content={'message': 'Invalid{}'.format(message), 'data': None})
