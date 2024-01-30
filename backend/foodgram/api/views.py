from django.shortcuts import render
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer, UserSignupSerializer
)
from recipes.models import (
    Tag, Ingredient, Recipe
)
from users.models import Follower
from .permissions import UserPermission


User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    http_method_names = ['get']


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    http_method_names = ['get']


class UserViewSet(UserViewSet):
    serializer_class = UserSignupSerializer
    queryset = User.objects.all()
    permission_classes = UserPermission

    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = serializer.data
            response_data['id'] = user.id
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = serializer.data
    #     for item in data:
    #         item['id'] = item['pk']
    #     return Response(data)

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAuthenticated]
    #     return [permission() for permission in permission_classes]
