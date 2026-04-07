from django.contrib import admin
from .models import Ingredient, Tool, Skill, Recipe, Allergy, RecipeIngredient, UserIngredient

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]

admin.site.register(Ingredient)
admin.site.register(Tool)
admin.site.register(Skill)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Allergy)
admin.site.register(UserIngredient)
