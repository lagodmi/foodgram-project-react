from datetime import datetime
from django.apps import apps
import pytest

from recipes.models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Shopping)
from users.models import User


COLORS_DICT = {
    'red': '#FF0000',
    'orange': '#FFA500',
    'yellow': '#FFFF00',
    'green': '#008000',
    'blue': '#0000FF',
    'indigo': '#4B0082',
    'violet': '#EE82EE',
    'black': '#000000',
    'white': '#FFFFFF',
    'gray': '#808080',
    'pink': '#FFC0CB'
}

UNITS_DICT = {
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
    for name, color in COLORS_DICT:
        tag_create_fix(name, color)


@pytest.fixture
def ingredient_create_fix(name='абрикосовое варенье', measurement_unit='г'):
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
        description='описание',
        image='tests/торт.webp',
        cooking_time=10,
        date=datetime.now()
    )

    apps.get_model('recipes', 'recipe_tag').objects.create(
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
    shopping = Shopping.objects.create(
        user=admin_user,
        recipe=recipe_create_fix
    )
    return shopping


@pytest.fixture
def user_create_fix():
    user = User.objects.create(
        username='Толстый_Лев',
        email='lion@mail.ru',
        first_name='Лев',
        last_name='Толстой',
        password='12345'
    )
    return user
