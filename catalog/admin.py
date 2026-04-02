from django.contrib import admin
from .models import Ingredient, Tool, Skill, Recipe, Allergy

admin.site.register(Ingredient)
admin.site.register(Tool)
admin.site.register(Skill)
admin.site.register(Recipe)
admin.site.register(Allergy)
