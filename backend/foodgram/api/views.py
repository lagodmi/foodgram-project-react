from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.status import (
    HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
)
from rest_framework.viewsets import (
    ModelViewSet, ReadOnlyModelViewSet
)

from .serializers import (
    TagSerializer, IngredientSerializer,
    RecipeSerializer, UserCreateSerializer,
    UserListSerializer, ChangePasswordSerializer
)
from recipes.models import (
    Tag, Ingredient, Recipe
)
from users.models import Follower
from .filters import NameFilter
from .pagination import CustomPagination


User = get_user_model()


class RecipeViewSet(ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    http_method_names = ['get']


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
