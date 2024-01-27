import pytest

from users.models import User


@pytest.mark.django_db
def test_create_user():
    assert User.objects.count() == 0
    User.objects.create(
        username='Толстый_Лев',
        email='lion@mail.ru',
        first_name='Лев',
        last_name='Толстой',
        password='12345'
    )
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_read_user(user_create_fix):
    user = User.objects.first()
    assert user.username == user_create_fix.username


@pytest.mark.django_db
def test_update_user(user_create_fix):
    user = User.objects.first()
    user.username = 'Тонкий_Лев'
    assert user.username == 'Тонкий_Лев'


@pytest.mark.django_db
def test_delete_user(user_create_fix):
    assert User.objects.count() == 1
    User.objects.first().delete()
    assert User.objects.count() == 0
