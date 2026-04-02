from django.shortcuts import render

#from .models import OUR MODELS HERE!!!

# Create your views here.
def index(request):
    """View function for home page of site. 
    This will collect the recipes, ingredients, and appliance/utensils 
    so they can be displayed to the user"""

    #allRecipes = Recipe.objects.all()
    #allIngredients = Ingredient.objects.all()
    #

    context = {
        #'allRecipes': allRecipes,
        #'allIngredients': allIngredients,
    }

    return render(request, 'index.html', context=context)


