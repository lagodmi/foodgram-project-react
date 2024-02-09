from drf_base64.fields import Base64ImageField
from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreateSerializer as UCSerializer,
    UserSerializer
)
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from recipes.models import (
    Tag,
    Favorite,
    Shopping,
    Recipe,
    RecipeIngredient,
    Ingredient
)
from users.models import Follower
from users.config import MAX_LEN_PASSWORD

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели тега.
    """

    class Meta:
        model = Tag
        fields = "__all__"


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели ингридиента.
    """

    class Meta:
        model = Ingredient
        fields = "__all__"


class UserCreateSerializer(UCSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password"
        )
        read_only_fields = ("id",)


class UserListSerializer(UserSerializer):
    """
    Сериалайзер для списка пользователей.
    """

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "is_subscribed"
        )

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and not request.user.is_anonymous:
            return (
                Follower.objects
                .filter(user=request.user, subscriber=obj)
                .exists()
            )
        return False


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Сериализатор смены пароля.
    """

    current_password = serializers.CharField(max_length=MAX_LEN_PASSWORD)
    new_password = serializers.CharField(max_length=MAX_LEN_PASSWORD)

    class Meta:
        model = User
        fields = ("current_password", "new_password")

    def update(self, instance, validated_data):
        if not instance.check_password(validated_data["current_password"]):
            raise serializers.ValidationError("Неправильный пароль.")
        instance.set_password(validated_data["new_password"])
        instance.save()
        return validated_data


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

    id = serializers.ReadOnlyField(source="ingredient.id")
    name = serializers.ReadOnlyField(source="ingredient.name")
    measurement_unit = (
        serializers.ReadOnlyField(source="ingredient.measurement_unit")
    )

    class Meta:
        model = RecipeIngredient
        fields = ("id", "amount", "name", "measurement_unit")


class RecipeListSerializer(serializers.ModelSerializer):
    """
    Сериаизатор списка рецептов.
    """

    author = UserListSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = (
        RecipeIngredientReadSerializer(many=True, source="recipeingredient")
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "tags",
            "image",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "author",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        return (
            user.is_authenticated
            and Favorite.objects.filter(user=user, recipe=obj).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        return (
            user.is_authenticated
            and Shopping.objects.filter(user=user, recipe=obj).exists()
        )


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели рецепта.
    """

    author = UserCreateSerializer(read_only=True)
    image = Base64ImageField()
    tags = (
        serializers.PrimaryKeyRelatedField(many=True,
                                           queryset=Tag.objects.all())
    )
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "name",
            "image",
            "text",
            "ingredients",
            "tags",
            "cooking_time",
        )

    def validate_ingredients(self, value):
        """
        Проверка наличия ингредиента.
        """
        if not value:
            raise serializers.ValidationError(
                "Поле 'ingredients' не может быть пустым."
            )
        return value

    @staticmethod
    def create_recipe_tags(self, recipe, tags):
        if len(tags) != len(set(tags)):
            raise serializers.ValidationError("В поле tags есть дубликаты.")
        if not tags:
            raise serializers.ValidationError("Поле tags не может быть пустым")
        recipe.tags.set(tags)

    @staticmethod
    def create_recipe_ingredients(self, recipe, ingredients):
        check_id = []
        for ingredient in ingredients:
            ingredient_id = ingredient.get("id")
            if ingredient_id in check_id:
                raise serializers.ValidationError("В ингредиентах дубликат.")
            check_id.append(ingredient_id)
            if ingredient.get("amount") < 1:
                raise serializers.ValidationError("Ошибка в поле amount")
            if ingredient_id:
                try:
                    ingredient_obj = Ingredient.objects.get(id=ingredient_id)
                except Ingredient.DoesNotExist:
                    raise serializers.ValidationError(
                        "Ингредиент с указанным id не найден."
                    )
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    amount=ingredient["amount"],
                    ingredient=ingredient_obj,
                )

    def create(self, validated_data):
        author = self.context.get("request").user
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_recipe_tags(self, recipe, tags_data)
        self.create_recipe_ingredients(self, recipe, ingredients_data)
        return recipe

    def update(self, instance, validated_data):

        if "ingredients" not in validated_data or "tags" not in validated_data:
            raise serializers.ValidationError(
                "Отсутствует обязательное поле tags или ingredients."
            )
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients", None)
        self.create_recipe_tags(self, instance, tags_data)
        if ingredients_data:
            instance.ingredients.clear()
            self.create_recipe_ingredients(self, instance, ingredients_data)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeListSerializer(instance, context=self.context).data


class RecipeShowSerializer(serializers.ModelSerializer):
    """
    Показ рецептов в урезанной форме.
    """

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class SubscribeSerializer(serializers.ModelSerializer):
    """
    Сериализатор подписок.
    """

    recipes_count = serializers.IntegerField(source="recipes.count",
                                             read_only=True)
    recipes = SerializerMethodField()
    is_subscribed = serializers.BooleanField(default=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "recipes_count",
            "recipes",
            "is_subscribed",
        )
        read_only_fields = ("email", "username", "first_name", "last_name")

    def get_recipes(self, obj):
        lim = self.context.get("recipes_limit")
        recipes = obj.recipes.all()[: int(lim)] if lim else obj.recipes.all()
        return (
            RecipeShowSerializer(recipes, many=True, context=self.context).data
        )

    def validate(self, data):
        author = self.context.get("author")
        user = self.context.get("request").user
        if user == author:
            raise serializers.ValidationError("Нельзя подписаться на себя.")
        return data


class ShoppingSerializer(serializers.ModelSerializer):
    """
    Сериализатор списка покупок.
    """

    class Meta:
        model = Shopping
        fields = ("id", "user", "recipe")
        read_only_fields = ("user", "recipe")

    def validate(self, data):
        user = self.context["request"].user
        recipe = self.context["recipe"]
        if user.shopping_man.filter(recipe=recipe).exists():
            raise serializers.ValidationError("Повторный рецепт.")
        return data

    def to_representation(self, instance):
        return RecipeShowSerializer(instance, context=self.context).data


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор избранных рецептов.
    """

    class Meta:
        model = Favorite
        fields = ("id", "user", "recipe")
        read_only_fields = ("user", "recipe")

    def validate(self, data):
        user = self.context["request"].user
        recipe = self.context["recipe"]
        if user.favorite_recipes.filter(recipe=recipe).exists():
            raise serializers.ValidationError("Рецепт уже в избранном.")
        return data

    def to_representation(self, instance):
        return RecipeShowSerializer(instance, context=self.context).data
