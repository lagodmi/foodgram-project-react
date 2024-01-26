import pytest


from recipes.models import (
    Tag, Ingredient, Recipe, RecipeIngredient, Favorite, Shopping)


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
def ingredient_create(name='red', color='#FF0000'):
    ingredient = Tag.objects.create(
        name=name,
        color=color
    )
    return ingredient
