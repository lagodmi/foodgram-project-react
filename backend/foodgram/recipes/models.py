from typing import Optional

from django.db import models

from users.models import User
from .constants import (
    MAX_LEN_NAME_TAG,
    MAX_LEN_COLOR_CODE_TAG,
    MAX_LEN_NAME_SLUG,
    MAX_LEN_NAME_INGREDIENT,
    MAX_LEN_UNIT_INGREDIENT,
    MAX_LEN_NAME_RECIPE,
    UPLOAD_TO_IMAGE_RECIPE,
)
from .validators import cooking_time_validator


class Tag(models.Model):
    """
    Модель тега.
    """

    name = models.CharField(
        verbose_name="Название тега",
        max_length=MAX_LEN_NAME_TAG,
        unique=True,
    )

    color = models.CharField(
        verbose_name="Цветовой код",
        max_length=MAX_LEN_COLOR_CODE_TAG,
        unique=True,
    )

    slug = models.SlugField(
        verbose_name="Слаг тега",
        max_length=MAX_LEN_NAME_SLUG,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        default_related_name = "tags"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель ингредиента.
    """

    name = models.CharField(
        verbose_name="Название",
        max_length=MAX_LEN_NAME_INGREDIENT,
    )

    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=MAX_LEN_UNIT_INGREDIENT,
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        default_related_name = "ingredients"
        ordering = ("name",)

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):

    def add_user_annotations(self, user_id: Optional[int]):
        return self.annotate(
            is_favorite=models.Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__pk=models.OuterRef("pk")
                )
            ),
        )


class Recipe(models.Model):
    """
    Модель рецепта.
    """

    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        verbose_name="Название",
        max_length=MAX_LEN_NAME_RECIPE,
    )

    image = models.ImageField(
        verbose_name="Картинка",
        upload_to=UPLOAD_TO_IMAGE_RECIPE,
    )

    text = models.TextField(
        verbose_name="Описание",
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name="Ингредиенты",
        through="RecipeIngredient",
        through_fields=("recipe", "ingredient"),
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тег",
        blank=False,
    )

    cooking_time = models.PositiveIntegerField(
        verbose_name="Время готовки", validators=(cooking_time_validator,)
    )

    date = models.DateTimeField(verbose_name="Дата публикации",
                                auto_now_add=True)

    objects = RecipeQuerySet.as_manager()

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        default_related_name = "recipes"
        ordering = ("-date",)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """
    Модель ингредиент в рецепте.
    """

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        on_delete=models.CASCADE,
    )

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name="Ингредиент",
        on_delete=models.CASCADE,
    )

    amount = models.PositiveIntegerField(verbose_name="Количество ингридиента")

    class Meta:
        verbose_name = "ингредиент в рецепте"
        verbose_name_plural = "ингредиенты в рецепте"
        default_related_name = "recipeingredient"

    def __str__(self):
        return f"{str(self.recipe)} - {str(self.ingredient)} {self.amount}"


class Shopping(models.Model):
    """
    Модель список покупок.
    """

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="shopping_man",
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        related_name="shopping_list",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Список Покупок"
        default_related_name = "shopping"

    def __str__(self):
        return self.recipe.name


class Favorite(models.Model):
    """
    Модель избранное.
    """

    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="favorite_recipes",
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        related_name="favorite_by",
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"), name="unique_favorite_user_recipe"
            )
        ]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        default_related_name = "favorite"
