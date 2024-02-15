from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Shopping,
    Favorite
)


admin.site.site_title = 'Админ-панель сайта "FOODGRAM"'
admin.site.site_header = 'Админ-панель сайта "FOODGRAM"'
admin.site.empty_value_display = "Не задано"


class BaseModelAdmin(admin.ModelAdmin):
    save_on_top = True
    save_as = True

    class Meta:
        abstract = True


@admin.register(Tag)
class TagAdmin(BaseModelAdmin):
    list_display = ("name", "color", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ingredient)
class IngredientAdmin(BaseModelAdmin):
    list_display = ("name", "measurement_unit")
    list_filter = ("name",)


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(BaseModelAdmin):
    list_filter = ("author", "name", "tags")
    inlines = (IngredientsInLine,)
    search_fields = (
        "author__username",
        "name",
    )
    list_display = ("name", "author")


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(BaseModelAdmin):
    list_display = ("recipe", "ingredient", "amount")


@admin.register(Shopping)
class ShoppingListAdmin(BaseModelAdmin):
    list_display = ("id", "user", "recipe")


@admin.register(Favorite)
class FavoriteListAdmin(BaseModelAdmin):
    list_display = ("user", "recipe")
