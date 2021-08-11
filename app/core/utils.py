from datetime import datetime, timedelta
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
