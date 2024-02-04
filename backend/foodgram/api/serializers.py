from drf_base64.fields import Base64ImageField
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from djoser.serializers import (UserCreateSerializer as UCSerializer,
                                UserSerializer)
from requests import Response
from rest_framework import serializers
from rest_framework.status import HTTP_401_UNAUTHORIZED

from recipes.models import (
    Tag, Favorite, Shopping,
    Recipe, RecipeIngredient,
    Ingredient
)
from users.models import Follower
from users.config import (
    MAX_LEN_PASSWORD
)

User = get_user_model()

ERROR_MESSAGE_SIGNUP = ('Поле {} не соответствует '
                        'пользователю с данным {}.')


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


class UserCreateSerializer(UCSerializer):
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


# RECIPE

class RecipeIngredientSerializer(serializers.Serializer):
    """
    Сериализатор для количества ингредиента.
    """
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipeIngredientReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиента в рецепте.
    """
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    # id = serializers.PrimaryKeyRelatedField(
    #     queryset=Ingredient.objects.all()
    # )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'amount',
            'name',
            'measurement_unit'
        )


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериаизатор списка рецептов.
    """
    author = UserListSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        many=True, source='recipeingredient')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags',
                  'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image',
                  'text', 'cooking_time')

    def get_is_favorited(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Favorite.objects.filter(user=self.context['request'].user,
                                        recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            self.context.get('request').user.is_authenticated
            and Shopping.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        )


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели рецепта.
    """
    author = UserCreateSerializer(read_only=True)
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name',
                  'image', 'text', 'ingredients',
                  'tags', 'cooking_time')

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                "Поле 'ingredients' не может быть пустым."
            )
        return value

    @staticmethod
    def create_recipe_tags(self, recipe, tags):
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError(
                        'В поле tags есть дубликаты.'
                    )
        print(tags)
        if not tags:
            raise serializers.ValidationError(
                        'Поле tags не может быть пустым'
                    )
        recipe.tags.set(tags)

    @staticmethod
    def create_recipe_ingredients(self, recipe, ingredients):
        check_id = []
        for ingredient in ingredients:
            ingredient_id = ingredient.get('id')
            if ingredient_id in check_id:
                raise serializers.ValidationError(
                        'В списке ингредиентов дубликат.'
                    )
            check_id.append(ingredient_id)
            if ingredient.get('amount') < 1:
                raise serializers.ValidationError(
                        'поле amount не может быть меньше 1'
                    )
            if ingredient_id:
                try:
                    ingredient_obj = Ingredient.objects.get(id=ingredient_id)
                except Ingredient.DoesNotExist:
                    raise serializers.ValidationError(
                        'Ингредиент с указанным id не найден.'
                    )
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    amount=ingredient['amount'],
                    ingredient=ingredient_obj
                )

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=self.context['request'].user,
                                       **validated_data)
        self.create_recipe_tags(self, recipe, tags_data)
        self.create_recipe_ingredients(self, recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):
        print(validated_data)
        recipe = instance
        if 'ingredients' not in validated_data or 'tags' not in validated_data:
            raise serializers.ValidationError(
                'Отсутствует обязательное поле tags или ingredients.'
            )
        self.create_recipe_tags(self, recipe, validated_data.pop('tags'))
        ingredients_data = validated_data.pop('ingredients', None)
        if ingredients_data:
            instance.ingredients.clear()
            self.create_recipe_ingredients(self, recipe, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance,
                                    context=self.context).data
