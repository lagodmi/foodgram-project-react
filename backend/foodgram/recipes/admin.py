from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Tag,
    Ingredient,
    Recipe
)


admin.site.site_title = 'Админ-панель сайта "FOODGRAM"'
admin.site.site_header = 'Админ-панель сайта "FOODGRAM"'
admin.site.empty_value_display = 'Не задано'


@admin.register(Tag)
class TegAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'color_code', 'slug'
    )
    list_editable = (
        'name', 'color_code', 'slug'
    )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'unit'
    )
    list_editable = (
        'name', 'unit'
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'name', 'get_html_photo', 'description', 'time', 'date'
    )
    list_editable = (
        'author', 'name', 'description', 'time'
    )

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src="{object.photo.url}" width=50>')

    get_html_photo.short_description = 'Миниатюра'
