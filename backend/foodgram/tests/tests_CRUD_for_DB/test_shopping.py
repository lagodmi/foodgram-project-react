import pytest

from recipes.models import Shopping


@pytest.mark.django_db
def test_create_shopping(admin_user, recipe_create_fix):
    assert Shopping.objects.count() == 0
    Shopping.objects.create(
        user=admin_user,
        recipe=recipe_create_fix
    )
    assert Shopping.objects.count() == 1


@pytest.mark.django_db
def test_read_shopping(shopping_create_fix):
    shopping = Shopping.objects.first()
    assert shopping.user == shopping_create_fix.user


@pytest.mark.django_db
def test_delete_shopping(shopping_create_fix):
    assert Shopping.objects.count() == 1
    Shopping.objects.first().delete()
    assert Shopping.objects.count() == 0
