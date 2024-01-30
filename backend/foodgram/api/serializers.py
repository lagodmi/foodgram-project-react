import re

from django.core.validators import validate_email
from django.db.models import Q
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from recipes.models import (
    Tag,
    Recipe,
    Ingredient
)

from users.models import Follower
from users.validators import user_validator
from users.config import (
    MAX_LEN_NICKNAME,
    MAX_LEN_EMAIL,
    MAX_LEN_NAME,
    MAX_LEN_SURNAME,
    MAX_LEN_PASSWORD
)

User = get_user_model()

ERROR_MESSAGE_SIGNUP = ('Поле {} не соответствует '
                        'пользователю с данным {}.')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели рецепта.
    """

    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели тега.
    """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ингридиента.
    """

    class Meta:
        model = Ingredient
        fields = '__all__'


class UserSignupSerializer(serializers.Serializer):
    """
    Сериализатор для регистрации пользователя.
    """
    email = serializers.EmailField(max_length=MAX_LEN_EMAIL)
    username = serializers.CharField(
        max_length=MAX_LEN_NICKNAME,
        validators=(user_validator,)
    )
    first_name = serializers.CharField(max_length=MAX_LEN_NAME)
    last_name = serializers.CharField(max_length=MAX_LEN_SURNAME)
    password = serializers.CharField(
        max_length=MAX_LEN_PASSWORD,
        write_only=True
    )

    def create(self, validated_data):
        user = validated_data.get('user')
        if user is None:
            user = User.objects.create(**validated_data)
        return user

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password = attrs.get('password')
        errors = {}
        users = User.objects.filter(
            Q(email=email) | Q(username=username)
        )
        if users:
            if not password:
                errors['password'] = 'Пароль отсутствует.'
            if any(user.username != username for user in users):
                errors['email'] = ERROR_MESSAGE_SIGNUP.format(
                    'username', 'email'
                )
            if any(user.email != email for user in users):
                errors['username'] = ERROR_MESSAGE_SIGNUP.format(
                    'email', 'username'
                )
            if errors:
                raise serializers.ValidationError(errors)
            attrs['user'] = users.first()
        return attrs
