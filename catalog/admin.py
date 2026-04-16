from django.contrib import admin
from .models import Ingredient, Tool, Skill, Recipe, Allergy, RecipeIngredient, UserIngredient, RecipeStep

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1
    ordering = ['order']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, RecipeStepInline]

admin.site.register(Ingredient)
admin.site.register(Tool)
admin.site.register(Skill)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Allergy)
admin.site.register(UserIngredient)
admin.site.register(RecipeStep)
