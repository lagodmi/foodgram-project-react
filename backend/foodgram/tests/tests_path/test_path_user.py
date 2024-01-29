import requests

from django.contrib.auth import get_user_model
import pytest


User = get_user_model()

NEW_USER = {
    "username": "Толстый_Лев",
    "email": "lion@mail.ru",
    "first_name": "Лев",
    "last_name": "Толстой",
    "password": "P@ssw0rd!2024"
}


@pytest.mark.django_db
def test_add_user(url_create_user_fix):
    response = requests.post(url_create_user_fix, json=NEW_USER)
    print(response.json())
    assert response.status_code == 201
