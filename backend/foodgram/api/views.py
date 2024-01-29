from django.shortcuts import render
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer, UserSignupSerializer
)
from recipes.models import (
    Tag, Ingredient, Recipe
)
from users.models import Follower


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

    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Сохраняем пользователя и получаем объект
            response_data = serializer.data  # Получаем данные сериализатора
            response_data['id'] = user.id  # Добавляем ID к данным ответа
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
