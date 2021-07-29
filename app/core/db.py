FakeDb = {
    'admin': {
        'username': 'admin',
        'password': 'EQu8KsnFs9X9lJhuU7rFgz4gIFT7qtLy24eDoDCOLh65ElVOWtZTV8BMalBpCMEw'
    }
}

def check_user_in_db(username, password):
    return True if FakeDb.get(username) and FakeDb.get(username).get("password") == password else False