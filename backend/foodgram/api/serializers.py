import re

from django.core.validators import validate_email
from djoser.views import UserViewSet
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.fields import SerializerMethodField

from recipes.models import (
    Tag,
    Recipe,
    Ingredient
)

from users.models import User, Follower


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


class UserSerializer(UserViewSet):

    """
    Сериализато для модели пользователя.
    """

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.get('user')
        if user is None:
            user = User.objects.create(**validated_data)
        return user
