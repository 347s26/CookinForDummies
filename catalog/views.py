from django.shortcuts import render
from django.views import generic
from django.views.generic import DetailView, TemplateView
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from catalog.forms import RecipeForm, RecipeIngredientFormSet, RecipeStepFormSet
from django.db.models import Q

from .models import Recipe, Ingredient, Tool, Skill, Allergy

class RecipeDetailView(DetailView):
    model = Recipe

def index(request):
    """View function for home page of site.
    Displays index page as the default home page."""

    featured_recipes = Recipe.objects.all()[:3]
    featured_skills = Skill.objects.all()[:3]
    featured_tools = Tool.objects.all()[:3]
    saved_recipes = []

    if request.user.is_authenticated:
        saved_recipes = request.user.saved_recipes.all()[:3]

    context = {
        'featured_recipes': featured_recipes,
        'featured_skills': featured_skills,
        'featured_tools': featured_tools,
        'saved_recipes': saved_recipes,
    }

    return render(request, 'index.html', context=context)


def signin_placeholder(request):
    """Display a non-functional placeholder sign-in page."""
    return render(request, 'signin_placeholder.html')


def about(request):
    """Display the about page."""
    return render(request, 'about.html')

# view function for recipe search
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
class MyRecipesView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/my_recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['created_recipes'] = Recipe.objects.filter(
            creator=self.request.user
        ).distinct()

        context['saved_recipes'] = Recipe.objects.filter(
            saved_by=self.request.user
        ).exclude(
            creator=self.request.user
        ).distinct()

        return context

# saving or removing recipes
@login_required
def toggle_save_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.creator == request.user:
        return redirect(recipe.get_absolute_url())

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

# for recipe form
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'catalog/recipe_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                self.request.POST,
                prefix='ingredient'
            )
            context['step_formset'] = RecipeStepFormSet(
                self.request.POST,
                prefix='step'
            )
        else:
            context['ingredient_formset'] = RecipeIngredientFormSet(prefix='ingredient')
            context['step_formset'] = RecipeStepFormSet(prefix='step')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        step_formset = context['step_formset']

        if ingredient_formset.is_valid() and step_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.creator = self.request.user
            self.object.save()

            ingredient_formset.instance = self.object
            ingredient_formset.save()

            step_formset.instance = self.object
            step_formset.save()

            return redirect(self.object.get_absolute_url())

        return self.render_to_response(self.get_context_data(form=form))



class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'catalog/recipe_form.html'

    def test_func(self):
        return self.get_object().creator == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                self.request.POST,
                instance=self.object,
                prefix='ingredient'
            )
            context['step_formset'] = RecipeStepFormSet(
                self.request.POST,
                instance=self.object,
                prefix='step'
            )
        else:
            context['ingredient_formset'] = RecipeIngredientFormSet(
                instance=self.object,
                prefix='ingredient'
            )
            context['step_formset'] = RecipeStepFormSet(
                instance=self.object,
                prefix='step'
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context['ingredient_formset']
        step_formset = context['step_formset']

        if ingredient_formset.is_valid() and step_formset.is_valid():
            self.object = form.save()

            ingredient_formset.instance = self.object
            ingredient_formset.save()

            step_formset.instance = self.object
            step_formset.save()

            return redirect(self.object.get_absolute_url())

        return self.render_to_response(self.get_context_data(form=form))


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    template_name = 'catalog/recipe_confirm_delete.html'
    success_url = reverse_lazy('my-recipes')

    def test_func(self):
        recipe = self.get_object()
        return recipe.creator == self.request.user
