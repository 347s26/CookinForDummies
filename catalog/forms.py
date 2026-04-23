from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient, RecipeStep

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time_to_make', 'rating', 'image_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity']
        widgets = {
            'ingredient': forms.Select(attrs={'class': 'ingredient-select'}),
        }

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    extra=1,
    can_delete=True
)

RecipeStepFormSet = inlineformset_factory(
    Recipe,
    RecipeStep,
    fields=['order', 'instruction'],
    extra=1,
    can_delete=True
)

