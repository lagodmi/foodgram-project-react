from django_filters.rest_framework import FilterSet, CharFilter
from django_filters.rest_framework.filters import ModelMultipleChoiceFilter
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class NameFilter(SearchFilter):
    """
    Фильтрация поля name  для ингридиентов.
    """
    search_param = 'name'


class RecipeFilter(FilterSet):
    author = CharFilter()
    tags = ModelMultipleChoiceFilter(field_name='tags__slug',
                                     to_field_name='slug',
                                     queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
