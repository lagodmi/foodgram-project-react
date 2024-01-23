from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe,
)


admin.site.site_title = 'Админ-панель сайта "FOODGRAM"'
admin.site.site_header = 'Админ-панель сайта "FOODGRAM"'
admin.site.empty_value_display = 'Не задано'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'measurement_unit'
    )
    list_editable = (
        'name', 'measurement_unit'
    )


class IngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    save_on_top = True  # бар сверху
    save_as = True  # бар 'сохранить как новый объект'
    list_filter = ('author',)  # фильтрация
    inlines = (IngredientsInLine,)
    search_fields = ('author__username', 'name',)  # поиск
    list_display = (
        'pk', 'author', 'name', 'cooking_time',
        'description', 'date',
    )
