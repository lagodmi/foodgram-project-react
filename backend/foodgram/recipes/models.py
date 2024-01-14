from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Teg(models.Model):
    """
    Модель тега.
    """
    pass


class Ingredient(models.Model):
    """
    Модель ингредиента.
    """
    pass


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name='Название',
        max_lenght=250,
    )

    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipes/',
    )

    description = models.TextField(
        verbose_name='Описание',
    )

    ingredient = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиент',
    )

    teg = models.ForeignKey(
        Teg,
        verbose_name='Тег'
    )

    time = models.PositiveIntegerField(
        verbose_name='Время'
    )
