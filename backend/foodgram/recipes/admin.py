from django.contrib import admin
from random import randint
# from django.utils.html import format_html

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


# >>>>>>>>>>>>>>>>>> late >>>>>>>>>>>
    # генератор цвета
# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'name', 'color', 'slug')
#     list_editable = ('name', 'color', 'slug')

#     def get_prepopulated_fields(self, request, obj=None):
#         return {'slug': ('name',), 'color': (self.random_color,)}

#     def random_color(self, obj):
#         def num() -> str: lambda: str(hex(randint(0, 255)))[2:].zfill(2)
#         return f'#{num()}{num()}{num()}'
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


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


# >>>>>>>>>>>>>>>>>>>late>>>>>>>>>>>>>
# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     save_on_top = True  # бар сверху
#     save_as = True  # бар 'сохранить как новый объект'
#     list_filter = ('author',)  # фильтрация
#     inlines = (IngredientsInLine,)
#     search_fields = ('author__username', 'name',)  # поиск
#     list_display = (
#         'pk', 'author', 'name', 'cooking_time',
#         'description', 'date',
#         'display_ingredients'
#     )

# реализация фото.
    # def get_img(self, object):
    #     """
    #     Отображаем картинку.
    #     """
    #     if object.image:
    #         return format_html(f'<img src="{object.image.url}" width=50>')

    # get_img.short_description = 'Миниатюра'  # отображение названия картинки

# отображение ингридиентов.
    # @admin.display(description='Ingredients')
    # def display_ingredients(obj):
    #     ingr_str = ', '.join(
    #         [
    #             ingredient.name for ingredient in obj.ingredients.all()
    #         ]
    #     )
    #     return ingr_str
# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
