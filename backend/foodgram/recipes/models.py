from django.contrib.auth import get_user_model
from django.db import models

from recipes.constants import (
    MAX_LEN_NAME_TAG,
    MAX_LEN_COLOR_CODE_TAG,
    MAX_LEN_NAME_SLUG,
    MAX_LEN_NAME_INGREDIENT,
    MAX_LEN_UNIT_INGREDIENT,
    MAX_LEN_NAME_RECIPE,
    UPLOAD_TO
)


User = get_user_model()


class Teg(models.Model):
    """
    Модель тега.
    """
    name = models.CharField(
        verbose_name='Название тега',
        max_length=MAX_LEN_NAME_TAG,
        unique=True,
    )

    color_code = models.CharField(
        verbose_name='Цветовой код',
        max_length=MAX_LEN_COLOR_CODE_TAG,
        unique=True,
    )

    slug = models.SlugField(
        verbose_name='Слаг',
        max_length=MAX_LEN_NAME_SLUG,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        default_related_name = 'tag'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель ингредиента.
    """
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LEN_NAME_INGREDIENT,
    )

    unit = models.SlugField(
        verbose_name='Единица измерения',
        max_length=MAX_LEN_UNIT_INGREDIENT,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        default_related_name = 'ingredient'
        ordering = ('pk',)

    def __str__(self):
        return self.name


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
        max_length=MAX_LEN_NAME_RECIPE,
    )

    image = models.ImageField(
        verbose_name='Картинка',
        upload_to=UPLOAD_TO,
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
        verbose_name='Тег',
        on_delete=models.CASCADE,
        blank=False,
    )

    time = models.PositiveIntegerField(
        verbose_name='Время'
    )

    date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipe'
        ordering = ('-date',)

    def __str__(self):
        return self.name
