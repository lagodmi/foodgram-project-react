from datetime import datetime
from django.apps import apps
import pytest

from recipes.models import Recipe, RecipeIngredient, Favorite


@pytest.mark.django_db
def test_create_recipe(admin_user, ingredient_create_fix, tag_create_fix):
    assert Recipe.objects.count() == 0
    recipe = Recipe.objects.create(
        author=admin_user,
        name='пирог',
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
    assert Recipe.objects.count() == 1


@pytest.mark.django_db
def test_read_recipe(recipe_create_fix):
    recipe = Recipe.objects.first()
    assert recipe.name == recipe_create_fix.name


@pytest.mark.django_db
def test_update_recipe(recipe_create_fix):
    recipe = Recipe.objects.first()
    recipe.name = 'торт'
    assert recipe.name == 'торт'


@pytest.mark.django_db
def test_delete_recipe(recipe_create_fix):
    assert Recipe.objects.count() == 1
    Recipe.objects.first().delete()
    assert Recipe.objects.count() == 0


@pytest.mark.django_db
def test_favorite_annotations(admin_user, recipe_create_fix):
    Favorite.objects.create(recipe=recipe_create_fix, user=admin_user)
    first_recipe = Recipe.objects.add_user_annotations(user_id=admin_user.id)
    assert first_recipe.values()[0]['is_favorite'] is True
