from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from .models import Recipe, Ingredient, Tool, Skill, Allergy

class RecipeDetailView(DetailView):
    model = Recipe

def index(request):
    """View function for home page of site. 
    Displays index page as the default home page."""

    #allRecipes = Recipe.objects.all()
    #allIngredients = Ingredient.objects.all()
    #

    context = {
        #'allRecipes': allRecipes,
        #'allIngredients': allIngredients,
    }

    return render(request, 'index.html', context=context)


def signin_placeholder(request):
    """Display a non-functional placeholder sign-in page."""
    return render(request, 'signin_placeholder.html')


def about(request):
    """Display the about page."""
    return render(request, 'about.html')

# #view function for recipe search
# def search_view(request):
    
#     recipes = Recipe.objects.all()

#     query = request.GET.get('q') # for title keyword search
#     max_time = request.GET.get('time') # for time filtering
#     min_rating = request.GET.get('rating') # for min ratign filtering

#     if query:
#         recipes = recipes.filter(title__icontains=query)

#     if max_time:
#         recipes = recipes.filter(time_to_make__lte=max_time)

#     if min_rating:
#         recipes = recipes.filter(rating__gte=min_rating)

#     context = {
#         'recipes': recipes,
#     }

#     return render(request, 'catalog/search.html', context)

# list view for recipe search
class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'catalog/search.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        """Filter recipes based on search input."""
        queryset = Recipe.objects.all()
        query = self.request.GET.get('q')
        max_time = self.request.GET.get('time')
        min_rating = self.request.GET.get('rating')

        if query:
            queryset = queryset.filter(title__icontains=query)
        if max_time:
            queryset = queryset.filter(time_to_make__lte=max_time)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        return queryset

# my recipes page
class MyRecipesView(LoginRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'catalog/my_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return self.request.user.saved_recipes.all()

# saving or removing recipes
@login_required
def toggle_save_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.user in recipe.saved_by.all():
        recipe.saved_by.remove(request.user)
    else:
        recipe.saved_by.add(request.user)

    return redirect(recipe.get_absolute_url())

def skills_view(request):
    skills = Skill.objects.all()

    context = {
        'skills': list(skills.values())
    }

    return render(request, 'skills.html', context)
