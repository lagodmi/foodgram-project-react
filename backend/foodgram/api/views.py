from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from requests import Response
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    SAFE_METHODS, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
)
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet
)

from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, RecipeListSerializer,
    UserCreateSerializer, UserListSerializer, ChangePasswordSerializer,
    SubscribeSerializer
)
from recipes.models import (
    Tag, Ingredient, Recipe
)
from users.models import Follower
from .filters import NameFilter, RecipeFilter
from .pagination import CustomPagination, CustomPaginationForSubscribe
from .permissions import IsOwnerOrReadOnly, IsAuthorOrReadOnly


User = get_user_model()


class UserViewSet(UserViewSet):
    """
    ViewSet пользователя.
    """
    queryset = User.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UserCreateSerializer
        return UserListSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'], pagination_class=None,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(status=HTTP_401_UNAUTHORIZED)
        return Response(
            UserListSerializer(request.user).data, status=HTTP_200_OK
        )

    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = ChangePasswordSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Пароль сохранен.', status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthorOrReadOnly,))
    def subscribe(self, request, **kwargs):
        if not request.user.is_authenticated:
            return Response("Требуется аутентификация пользователя",
                            status=HTTP_401_UNAUTHORIZED)

        author = get_object_or_404(User, id=kwargs['id'])
        recipes_limit = request.query_params.get('recipes_limit', None)
        context = {'request': request, 'author': author,
                   'recipes_limit': recipes_limit}
        serializer = SubscribeSerializer(author, data=request.data,
                                         context=context)

        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            if Follower.objects.filter(user=request.user,
                                       subscriber=author).exists():
                return Response('Подписка уже оформлена.',
                                status=HTTP_400_BAD_REQUEST)
            else:
                Follower.objects.create(user=request.user, subscriber=author)
                return Response(serializer.data, status=HTTP_201_CREATED)

    @action(detail=False, permission_classes=(IsAuthorOrReadOnly,))
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribers__user=user)
        page = self.paginate_queryset(queryset)
        recipes_limit = request.query_params.get('recipes_limit', None)
        context = {'request': request, 'recipes_limit': recipes_limit}
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
    search_fields = ('^name',)
    http_method_names = ('get',)


class RecipeViewSet(ModelViewSet):
    """
    ViewSet рецепта.
    """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)
