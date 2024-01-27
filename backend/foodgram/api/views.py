from django.shortcuts import render
from rest_framework import viewsets

from .serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer
)
from recipes.models import (
    Tag, Ingredient, Recipe
)


class TagViewset(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewset(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewset(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
