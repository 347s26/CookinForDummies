from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),,
    path('signin-placeholder/', views.signin_placeholder, name='signin-placeholder'),
    path('about/', views.about, name='about'),
    #path('search/', views.search_view, name='search'),
    path('search/', views.RecipeSearchView.as_view(), name='search'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
]
