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
from django.conf import settings
from django.utils import timezone
import requests
from django.utils.dateparse import parse_date

from .models import Recipe, Ingredient, Tool, Skill, Allergy
from .models import UserIngredient

class RecipeDetailView(DetailView):
    model = Recipe


def generate_ai_cooking_help(user_prompt):
    api_key = getattr(settings, 'LLM_API_KEY', '')
    if not api_key:
        return None, 'LLM API key is not configured. Set OPENROUTER_API_KEY in your environment.'

    model_name = getattr(settings, 'LLM_MODEL', 'meta-llama/llama-3.1-8b-instruct:free')
    endpoint = getattr(settings, 'LLM_API_URL', 'https://openrouter.ai/api/v1/chat/completions')

    messages = [
        {
            'role': 'system',
            'content': (
                'You are a cooking name suggester. Return only short dish names. '
                'Never include ingredients, steps, explanations, or full recipes. '
                'Return 3 to 6 dish names, one per line, and keep each line under 6 words.'
            )
        },
        {'role': 'user', 'content': user_prompt}
    ]

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    models_to_try = [model_name]
    if model_name != 'openrouter/auto':
        models_to_try.append('openrouter/auto')

    last_error = None
    for candidate_model in models_to_try:
        payload = {
            'model': candidate_model,
            'messages': messages,
            'temperature': 0.7,
            'max_tokens': 350,
        }

        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=20)
            if response.ok:
                data = response.json()
                text = data['choices'][0]['message']['content'].strip()
                # Safety clamp: keep the response short and list-like.
                lines = [line.strip('-* \t') for line in text.splitlines() if line.strip()]
                lines = [line for line in lines if len(line.split()) <= 8]
                if not lines:
                    lines = [text[:80]]
                text = '\n'.join(lines[:6])
                return text, None

            error_message = response.text
            try:
                error_json = response.json()
                error_message = error_json.get('error', {}).get('message', error_message)
            except Exception:
                pass

            last_error = f'HTTP {response.status_code}: {error_message}'
        except Exception as exc:
            last_error = str(exc)

    return None, f'LLM request failed: {last_error}'

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
    ai_response = None
    ai_error = None
    user_prompt = ''

    if request.method == 'POST':
        user_prompt = (request.POST.get('ai_prompt') or '').strip()
        if len(user_prompt) < 4:
            ai_error = 'Please enter a slightly longer question so I can help.'
        elif len(user_prompt) > 500:
            ai_error = 'Please keep the question under 500 characters.'
        else:
            ai_response, ai_error = generate_ai_cooking_help(user_prompt)

    return render(request, 'about.html', {
        'ai_response': ai_response,
        'ai_error': ai_error,
        'ai_prompt': user_prompt,
    })

# view function for recipe search
class RecipeSearchView(ListView):
    model = Recipe
    template_name = 'catalog/search.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        """Filter recipes based on search input."""
        queryset = Recipe.objects.filter(creator__isnull=True)
        query = self.request.GET.get('q')
        max_time = self.request.GET.get('time')
        min_rating = self.request.GET.get('rating')
        pantry_ingredient = (self.request.GET.get('ingredient') or '').strip()
        pantry_ingredient_new = (self.request.GET.get('ingredient_new') or '').strip()

        if pantry_ingredient == '__new__':
            pantry_ingredient = pantry_ingredient_new

        if query:
            queryset = queryset.filter(title__icontains=query)
        if max_time:
            queryset = queryset.filter(time_to_make__lte=max_time)
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)

        if pantry_ingredient:
            queryset = queryset.filter(ingredients__name__iexact=pantry_ingredient)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['pantry_ingredients'] = list(
                UserIngredient.objects.filter(user=self.request.user)
                .select_related('ingredient')
                .order_by('ingredient__name')
                .values_list('ingredient__name', flat=True)
                .distinct()
            )
        else:
            context['pantry_ingredients'] = []
        return context

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


def delete_expired_user_ingredients(user):
    """Remove pantry items whose expiration date is in the past."""
    today = timezone.localdate()
    UserIngredient.objects.filter(user=user, expiration_date__lt=today).delete()

def skills_view(request):
    skills = Skill.objects.all()

    context = {
        'skills': list(skills.values())
    }

    return render(request, 'skills.html', context)


@login_required
def my_ingredients(request):
    """Show and update the user's pantry ingredients."""
    delete_expired_user_ingredients(request.user)

    if request.method == 'POST':
        ingredient_name = (request.POST.get('ingredient_name') or '').strip()
        ingredient_name_new = (request.POST.get('ingredient_name_new') or '').strip()
        quantity = (request.POST.get('quantity') or '').strip()
        location = (request.POST.get('location') or '').strip()
        expiration_date_raw = (request.POST.get('expiration_date') or '').strip()

        if ingredient_name == '__new__':
            ingredient_name = ingredient_name_new

        if ingredient_name:
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            pantry_item, _ = UserIngredient.objects.get_or_create(
                user=request.user,
                ingredient=ingredient,
            )
            pantry_item.quantity = quantity
            pantry_item.location = location
            pantry_item.expiration_date = parse_date(expiration_date_raw) if expiration_date_raw else None
            pantry_item.save()

        delete_expired_user_ingredients(request.user)

        return redirect('my-ingredients')

    items = UserIngredient.objects.filter(user=request.user).select_related('ingredient').order_by('ingredient__name')
    ingredient_choices = list(
        Ingredient.objects.filter(recipeingredient__isnull=False)
        .distinct()
        .order_by('name')
        .values_list('name', flat=True)
    )
    return render(request, 'my_ingredients.html', {
        'items': items,
        'ingredient_choices': ingredient_choices,
    })


@login_required
def delete_my_ingredient(request, pk):
    """Delete one pantry ingredient owned by the current user."""
    pantry_item = get_object_or_404(UserIngredient, pk=pk, user=request.user)
    if request.method == 'POST':
        pantry_item.delete()
    return redirect('my-ingredients')

# for recipe form
class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'catalog/recipe_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs['files'] = self.request.FILES
        return kwargs

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
