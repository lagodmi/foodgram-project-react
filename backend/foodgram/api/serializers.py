from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from recipes.models import (
    Tag,
    Recipe,
    Ingredient
)
from users.models import Follower
from users.config import (
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


class UserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'password')
        read_only_fields = ('id',)


class UserListSerializer(UserSerializer):
    """
    Сериалайзер для списка пользователей.
    """
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        # Проверяем, подписан ли текущий пользователь на пользователя obj
        request = self.context.get('request')
        if request and not request.user.is_anonymous:
            return (Follower.objects.
                    filter(user=request.user, subscriber=obj).exists())
        return False


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Сериализатор смены пароля.
    """
    current_password = serializers.CharField(max_length=MAX_LEN_PASSWORD)
    new_password = serializers.CharField(max_length=MAX_LEN_PASSWORD)

    class Meta:
        model = User
        fields = ('current_password', 'new_password')

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data['current_password']):
            raise serializers.ValidationError('Неправильный пароль.')
        instance.set_password(validated_data['new_password'])
        instance.save()
        return validated_data
