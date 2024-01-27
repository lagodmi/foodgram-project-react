from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TagViewset, IngredientViewset, RecipeViewset
)

router = DefaultRouter()

router.register('tags', viewset=TagViewset, basename='tag')
# router.register('ingredients', viewset=IngredientViewset,
#                 basename='ingredient')
# router.register('recipes', viewset=RecipeViewset, basename='recipe')

urlpatterns = [
    path('', include(router.urls))
]
