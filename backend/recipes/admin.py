from django.contrib import admin

from .models import Tag, Recipe, Ingredient, RecipeIngredients


@admin.register(Tag)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


@admin.register(Recipe)
class AdminRecipe(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')


@admin.register(Ingredient)
class AdminTag(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')


@admin.register(RecipeIngredients)
class AdminTag(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')
