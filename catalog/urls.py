from django.urls import path
from . import views
from .views import RecipeCreateView, RecipeUpdateView, RecipeDeleteView 

urlpatterns = [
    path('', views.index, name='index'),
    path('signin-placeholder/', views.signin_placeholder, name='signin-placeholder'),
    path('about/', views.about, name='about'),
    #path('search/', views.search_view, name='search'),
    path('search/', views.RecipeSearchView.as_view(), name='search'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('skills/', views.skills_view, name='skills'),
    path('my-ingredients/', views.my_ingredients, name='my-ingredients'),
    path('my-ingredients/<int:pk>/delete/', views.delete_my_ingredient, name='my-ingredient-delete'),
    path('my-recipes/', views.MyRecipesView.as_view(), name='my-recipes'),
    path('recipe/<int:pk>/save/', views.toggle_save_recipe, name='toggle-save-recipe'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path('recipe/<int:pk>/edit/', RecipeUpdateView.as_view(), name='recipe-edit'),
    path('recipe/<int:pk>/delete/', RecipeDeleteView.as_view(), name='recipe-delete'),
    path('recipe/<int:pk>/rate/', views.rate_recipe, name='rate-recipe'),
]
