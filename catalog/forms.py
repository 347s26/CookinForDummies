from django.forms import ModelForm
from catalog.models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["title", "description", "ingredients", "time_to_make", "image_url"]



#inlineformset_factory for ingredients and steps?

