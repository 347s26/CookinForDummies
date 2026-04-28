from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeIngredient, RecipeStep
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time_to_make', 'rating', 'image']
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

class BaseRecipeIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        seen = set()

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                ingredient = form.cleaned_data.get('ingredient')

                if ingredient in seen:
                    raise ValidationError("You can only select each ingredient once.")
                
                seen.add(ingredient)

RecipeIngredientFormSet = inlineformset_factory(
    Recipe,
    RecipeIngredient,
    form=RecipeIngredientForm,
    formset=BaseRecipeIngredientFormSet,
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

