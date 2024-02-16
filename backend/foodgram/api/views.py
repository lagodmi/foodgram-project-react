from django.db.models.aggregates import Sum
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeSerializer,
    UserCreateSerializer,
    UserListSerializer,
    ChangePasswordSerializer,
    SubscribeSerializer,
    ShoppingSerializer,
    FavoriteSerializer,
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Shopping,
    RecipeIngredient,
    Favorite
)
from users.models import Follower
from .filters import NameFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly


User = get_user_model()


class UserViewSet(UserViewSet):
    """
    ViewSet пользователя.
    """

    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        return (AllowAny(),)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return UserCreateSerializer
        return UserListSerializer

    @action(
        detail=False,
        pagination_class=None,
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return Response(UserListSerializer(request.user).data,
                        status=HTTP_200_OK)

    @action(
        detail=False,
        methods=("post",),
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = ChangePasswordSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Пароль сохранен.", status=HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthorOrReadOnly,),
    )
    def subscribe(self, request, id):
        if not request.user.is_authenticated:
            return Response(
                "Требуется аутентификация пользователя.",
                status=HTTP_401_UNAUTHORIZED
            )

        author = get_object_or_404(User, id=id)
        user = request.user
        user_filter = user.owner.filter(subscriber=author)

        recipes_limit = request.query_params.get("recipes_limit", None)
        context = {
            "request": request,
            "author": author,
            "recipes_limit": recipes_limit
        }
        serializer = (
            SubscribeSerializer(author, data=request.data, context=context)
        )

        if request.method == "POST":
            serializer.is_valid(raise_exception=True)

            if user_filter.exists():
                return Response("Подписка уже оформлена.",
                                status=HTTP_400_BAD_REQUEST)
            Follower.objects.create(user=user, subscriber=author)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if not user_filter:
            return Response("Подписка отсутствует.",
                            status=HTTP_400_BAD_REQUEST)
        user_filter.delete()
        return Response("Подписка успешно удалена.",
                        status=HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=(IsAuthorOrReadOnly,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        page = self.paginate_queryset(queryset)
        recipes_limit = request.query_params.get("recipes_limit", None)
        context = {"request": request, "recipes_limit": recipes_limit}
        serializer = SubscribeSerializer(page, many=True, context=context)
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    """
    ViewSet тега.
    """

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ModelViewSet):
    """
    ViewSet ингридиента.
    """

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    filter_backends = (NameFilter,)
    search_fields = ("^name",)
    http_method_names = ("get",)


class RecipeViewSet(ModelViewSet):
    """
    ViewSet рецепта.
    """

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        user = self.request.user

        if self.request.method == "POST":
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response("Рецепт отсутствует.",
                                status=HTTP_400_BAD_REQUEST)
            serializer = ShoppingSerializer(
                recipe,
                data=request.data,
                context={"request": request, "recipe": recipe},
            )
            serializer.is_valid(raise_exception=True)

            Shopping.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)

        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response("Рецепт отсутствует.", status=HTTP_404_NOT_FOUND)

        try:
            Shopping.objects.get(user=user, recipe=recipe).delete()
            return Response(
                "Рецепт успешно удален из корзины.", status=HTTP_204_NO_CONTENT
            )
        except Shopping.DoesNotExist:
            return Response(
                "Рецепт отсутствует в корзине.", status=HTTP_400_BAD_REQUEST
            )

    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__shopping_list__user=request.user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(amount=Sum("amount"))
        )
        text = "Список покупок:\n"
        for ingredient in ingredients:
            text += (
                f'- {ingredient["ingredient__name"]}'
                f' {ingredient["amount"]}'
                f' {ingredient["ingredient__measurement_unit"]}\n'
            )
        return HttpResponse(
            text,
            content_type="text/plain; charset=UTF-8",
            headers={"Content-Disposition": "attachment; filename=buying.txt"},
        )

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        user = self.request.user

        if request.method == "POST":
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response("Рецепт отсутствует.",
                                status=HTTP_400_BAD_REQUEST)
            serializer = FavoriteSerializer(
                recipe,
                data=request.data,
                context={"request": request, "recipe": recipe},
            )
            serializer.is_valid(raise_exception=True)
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)

        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response("Рецепт отсутствует.", status=HTTP_404_NOT_FOUND)
        user_filter = user.favorite_recipes.filter(recipe=recipe)

        if not user_filter:
            return Response("Рецепт отсутствует в избранном.",
                            status=HTTP_400_BAD_REQUEST)
        user_filter.delete()
        return Response("Рецепт успешно удален из избранного.",
                        status=HTTP_204_NO_CONTENT)
