from django.contrib import admin

from .models import (
    Tag,
    Ingredient,
    Recipe
)


admin.site.empty_value_display = 'Не задано'


# @admin.register(Teg)
# class TegAdmin(admin.ModelAdmin):
#     list_display = ('__all__',)
#     list_editable = ('__all__',)


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     list_display = ('__all__',)
#     list_editable = ('__all__',)


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('__all__',)
#     list_editable = ('__all__',)


class BaseModelAdmin(admin.ModelAdmin):
    list_display = ('__all__',)
    list_editable = ('__all__',)

    class Meta:
        abstract = True


@admin.register(Tag)
class TegAdmin(BaseModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(BaseModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(BaseModelAdmin):
    filter_horizontal = ('ingredient','tag')
