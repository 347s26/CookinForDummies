from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('search/', views.search_view, name='search'),
    path('search/', views.RecipeSearchView.as_view(), name='search'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
]
