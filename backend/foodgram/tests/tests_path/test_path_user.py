import copy
import requests

from django.contrib.auth import get_user_model
import pytest


User = get_user_model()

USERS_LIST: list[dict] = [
    {
        'username': 'TolstoyLion',
        'email': 'li@mail.ru',
        'first_name': 'Leo',
        'last_name': 'Tolstoy',
        'password': 'PUkf$12345'
    },
    {
        'username': 'WarAndPeaceFan',
        'email': 'leo@gmail.com',
        'first_name': 'Lev',
        'last_name': 'Tolstoy',
        'password': '$$kufGG54321'
    },
    {
        'username': 'LeoWriter',
        'email': 'ltolstoy@yahoo.com',
        'first_name': 'Lev',
        'last_name': 'Tolstoy',
        'password': '$8345IIIqwerty'
    },
]

LIST_CONTEXT: list[dict] = [
    {'email': 'li@mail.ru',
     'password': 'PUkf$12345'},
    {'email': 'leo@gmail.com',
     'password': '$$kufGG54321'}
]

USER: dict = {
    'username': 'VasiyPupkin',
    'email': 'vasiypupkin@mail.ru',
    'first_name': 'Vasiy',
    'last_name': 'Pupkin',
    'password': 'PUkf$123kkGG45'
}


@pytest.mark.django_db
def test_create_user():
    """
    Тест на регистрацию трех пользователей.
    """
    url = "http://127.0.0.1:8000/api/users/"
    for user in USERS_LIST:
        response = requests.post(url, json=user)
        print(response.json())
        assert response.status_code == 201


@pytest.mark.django_db
def test_get_token():
    """
    Тест на получение токена двум пользователям.
    """
    url = 'http://127.0.0.1:8000/api/auth/token/login/'
    for context in LIST_CONTEXT:
        response = requests.post(url, json=context)
        assert response.status_code == 200


def test_get_token_no_row():
    """
    Тест на получение токена с отсутствующими email или password.
    """
    url = 'http://127.0.0.1:8000/api/auth/token/login/'
    context = LIST_CONTEXT[0]
    for key in list(context.keys()):
        modified_context = copy.deepcopy(LIST_CONTEXT[0])
        modified_context.pop(key)
        response = requests.post(url, json=modified_context)
        assert response.status_code == 400


def test_get_token_wrong_password():
    """
    Тест на получение токена с неправильным password.
    """
    url = 'http://127.0.0.1:8000/api/auth/token/login/'
    modified_context = copy.deepcopy(LIST_CONTEXT[0])
    modified_context['password'] = 'randompassword'
    response = requests.post(url, json=modified_context)
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_register_without_row():
    """
    Тест на проверку отсутствия поля.
    """
    url = "http://127.0.0.1:8000/api/users/"
    for key in USER.keys():
        modified_user = copy.deepcopy(USER)
        modified_user.pop(key)
        response = requests.post(url, json=modified_user)
        assert response.status_code == 400


@pytest.mark.django_db
def test_user_register_without_long_row():
    """
    Тест на проверку длинного поля.
    """
    url = "http://127.0.0.1:8000/api/users/"
    long = """looooooooooooooooooooooooooooooooooooooooooooooo
    ooooooooooooooooooooooooooooooooooooooooooooooooooooooong"""
    for key in USER.keys():
        modified_user = copy.deepcopy(USER)
        modified_user[key] += long
        response = requests.post(url, json=modified_user)
        assert response.status_code == 400


@pytest.mark.django_db
def test_user_register_row_in_use():
    """
    Тест на проверку занятого поля.
    """
    url = "http://127.0.0.1:8000/api/users/"
    test_rows = {
        'username': 'TolstoyLion',
        'email': 'li@mail.ru',
    }
    for key, value in test_rows.items():
        modified_user = copy.deepcopy(USER)
        modified_user[key] = value
        response = requests.post(url, json=modified_user)
        assert response.status_code == 400


@pytest.mark.django_db
def test_user_register_invalid_username():
    """
    Тест на проверку неправильного поля username.
    """
    url = "http://127.0.0.1:8000/api/users/"
    modified_user = copy.deepcopy(USER)
    modified_user['username'] = "InvalidU$ername"
    response = requests.post(url, json=modified_user)
    assert response.status_code == 400


def test_protected_endpoint(auth_token):
    url = 'http://example.com/api/protected_endpoint'
    headers = {
        'Authorization': f'Token {auth_token}'
    }

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
