from datetime import datetime
import requests

from django.apps import apps
from django.contrib.auth import get_user_model
import pytest

from recipes.models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Shopping)
from tests.constants import USER


User = get_user_model()


# Fixture for CRUD DB.


TAGS_DICT: dict = {
    'обед': '#FF0000',
    'завтрак': '#FFA500',
    'полдник': '#FFFF00',
    'перекус': '#008000',
    'ужин': '#0000FF',
    'ланч': '#4B0082',
    'поздний ужин': '#EE82EE',
    'чай': '#000000',
    'десерт': '#FFFFFF',
    'выпечка': '#808080',
    'сладкое': '#FFC0CB'
}

UNITS_DICT: dict = {
    "абрикосовое варенье": "г",
    "абрикосовое пюре": "г",
    "абрикосовый джем": "г",
    "абрикосовый сок": "стакан",
    "абрикосы": "г",
    "абрикосы консервированные": "г",
    "авокадо": "по вкусу",
    "агава сироп": "г",
    "агар-агар": "г",
    "аграм": "г",
    "аджика": "г"
}


@pytest.fixture
def tag_create_fix(name='red', color='#FF0000'):
    """
    Фикстура на создание одного тега.
    """
    tag = Tag.objects.create(
        name=name,
        color=color
    )
    return tag


@pytest.fixture
def tags_create_fix():
    """
    Фикстура на создание списка тегов.
    Проверка пагинации.
    """
    for name, color in TAGS_DICT:
        tag_create_fix(name, color)


@pytest.fixture
def ingredient_create_fix(name='абрикосовое варенье', measurement_unit='г'):
    """
    Фикстура на создание одного ингредиента.
    """
    ingredient = Ingredient.objects.create(
        name=name,
        measurement_unit=measurement_unit
    )
    return ingredient


@pytest.fixture
def ingredients_create_fix():
    """
    Фикстура на создание списка ингредиентов.
    Проверка пагинации.
    """
    for name, measurement_unit in UNITS_DICT:
        ingredient_create_fix(name, measurement_unit)


@pytest.fixture
def recipe_create_fix(
    admin_user, ingredient_create_fix, tag_create_fix, name='пирог'
):
    """
    Фикстура на создание одного рецепта.
    """
    recipe = Recipe.objects.create(
        author=admin_user,
        name=name,
        text='описание',
        image='tests/торт.webp',
        cooking_time=10,
        date=datetime.now()
    )

    apps.get_model('recipes', 'recipe_tags').objects.create(
        recipe=recipe,
        tag=tag_create_fix
    )

    RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient_create_fix,
        amount=1
    )
    return recipe


@pytest.fixture
def shopping_create_fix(admin_user, recipe_create_fix):
    """
    Фикстура на добавление рецепта в корзину.
    """
    shopping = Shopping.objects.create(
        user=admin_user,
        recipe=recipe_create_fix
    )
    return shopping


@pytest.fixture
def user_create_fix():
    """
    Фикстура на создание пользователя.
    """
    user = User.objects.create(
        username='Толстый_Лев',
        email='lion@mail.ru',
        first_name='Лев',
        last_name='Толстой',
        password='12345'
    )
    return user


# Fixture check URL.


@pytest.fixture
def auth_token():
    """
    Фикстура на получение токена.
    """
    url = 'http://127.0.0.1:8000/api/auth/token/login/'
    credentials = {
        'email': USER['email'],
        'password': USER['password']
    }

    response = requests.post(url, json=credentials)
    token = response.json().get('auth_token')
    return token
