from django_filters.rest_framework import CharFilter, FilterSet
from django_filters.rest_framework.filters import (
    BooleanFilter,
    ModelMultipleChoiceFilter,
)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag


class NameFilter(SearchFilter):
    """
    Фильтрация поля name  для ингридиентов.
    """

    search_param = "name"


class RecipeFilter(FilterSet):
    """
    Фильтр для рецептов.
    """

    is_in_shopping_cart = BooleanFilter(method="filter_by_shopping_cart")
    is_favorited = BooleanFilter(method="filter_by_favorited")
    author = CharFilter()
    tags = ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all()
    )

    def filter_by_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset

    def filter_by_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite_by__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ("author", "tags", "is_in_shopping_cart", "is_favorited")
