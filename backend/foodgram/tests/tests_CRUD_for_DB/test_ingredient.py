import pytest

from recipes.models import Ingredient


@pytest.mark.django_db
def test_create_ingredient():
    assert Ingredient.objects.count() == 0
    Ingredient.objects.create(
        name='абрикосовое варенье',
        measurement_unit='г'
    )
    assert Ingredient.objects.count() == 1


@pytest.mark.django_db
def test_read_ingredient(ingredient_create_fix):
    ingredient = Ingredient.objects.first()
    assert ingredient.name == ingredient_create_fix.name


@pytest.mark.django_db
def test_update_ingredient(ingredient_create_fix):
    ingredient = Ingredient.objects.first()
    ingredient.measurement_unit = 'ст. л.'
    assert ingredient.measurement_unit == 'ст. л.'


@pytest.mark.django_db
def test_delete_ingredient(ingredient_create_fix):
    assert Ingredient.objects.count() == 1
    Ingredient.objects.first().delete()
    assert Ingredient.objects.count() == 0
