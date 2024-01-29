from django.shortcuts import render
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer, UserSerializer
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
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # def post(self, request, *args, **kwargs):
        # response = super().post(request, *args, **kwargs)
        # response.status_code = status.HTTP_200_OK
        # return response
