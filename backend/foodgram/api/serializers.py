from rest_framework.serializers import ModelSerializer

from recipes.models import (
    Tag,
    Recipe,
    Ingredient
)


class RecipeSerializer(ModelSerializer):
    """
    Сериализатор для модели рецепта.
    """

    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(ModelSerializer):
    """
    Сериализатор для модели тега.
    """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    """
    Сериализатор для модели ингридиента.
    """

    class Meta:
        model = Ingredient
        fields = '__all__'
