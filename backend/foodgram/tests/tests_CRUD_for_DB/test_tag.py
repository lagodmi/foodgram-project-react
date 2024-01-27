import pytest

from recipes.models import Tag


@pytest.mark.django_db
def test_create_tag():
    assert Tag.objects.count() == 0
    Tag.objects.create(
        name='red',
        color='FF0000'
    )
    assert Tag.objects.count() == 1


@pytest.mark.django_db
def test_read_tag(tag_create_fix):
    tag = Tag.objects.first()
    assert tag.name == tag_create_fix.name


@pytest.mark.django_db
def test_update_tag(tag_create_fix):
    tag = Tag.objects.first()
    tag.name = 'красный'
    assert tag.name == 'красный'


@pytest.mark.django_db
def test_delete_tag(tag_create_fix):
    assert Tag.objects.count() == 1
    Tag.objects.first().delete()
    assert Tag.objects.count() == 0
