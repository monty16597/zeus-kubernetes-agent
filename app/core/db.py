from .config import ADMIN_USERNAME, ADMIN_PASSWORD

FakeDb = {
    ADMIN_USERNAME: {
        'username': ADMIN_USERNAME,
        'password': ADMIN_PASSWORD
    }
}


def check_user_in_db(username, password):
    return True if FakeDb.get(username) and FakeDb.get(username).get('password') == password else False
