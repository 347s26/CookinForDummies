from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView
from django.views.generic import ListView

from .models import Recipe, Ingredient, Tool, Skill, Allergy

class RecipeDetailView(DetailView):
    model = Recipe

def index(request):
    """View function for home page of site.
    Displays index page as the default home page."""

    featured_recipes = Recipe.objects.all()[:3]
    featured_skills = Skill.objects.all()[:3]
    featured_tools = Tool.objects.all()[:3]

    context = {
        'featured_recipes': featured_recipes,
        'featured_skills': featured_skills,
        'featured_tools': featured_tools,
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


def skills_view(request):
    skills = Skill.objects.all()

    context = {
        'skills': list(skills.values())
    }

    return render(request, 'skills.html', context)
