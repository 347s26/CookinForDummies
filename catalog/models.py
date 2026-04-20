import uuid
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
    "Model representing an ingredient"
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter an ingredient(e.g. Onion, Lemon, etc.)"
    )

    def __str__(self):
        "String for representing the model object"
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='ingredient_name_case_insensitive_unique'
            ),
        ]

class Tool(models.Model):
    "Model representing a Tool"
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a Tool(e.g. Knife, Pan, etc.)"
    )

    def __str__(self):
        "String for representing the model object"
        return self.name

class Skill(models.Model):
    """Model representing a Skill."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a skill(e.g. dicing onions, caramelizing onions, etc)"
    )
    video = models.URLField(blank=True, null=True)

    def __str__(self):
        "String for representing the model object"
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )

    tools = models.ManyToManyField(
        Tool,
        blank=True
    )

    skills = models.ManyToManyField(
        Skill,
        blank=True
    )

    time_to_make = models.IntegerField(
        help_text="Time in minutes"
    )

    rating = models.IntegerField(
        blank=True,
        null=True
    )

    saved_by = models.ManyToManyField(
        User,
        blank=True,
        related_name='saved_recipes'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])

# for seperate steps
class RecipeStep(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_steps'
    )

    order = models.IntegerField()

    instruction = models.TextField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Step {self.order} for {self.recipe.title}"

class Allergy(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter an Allergy(e.g. nuts, berries etc.)"
    )

    Ingredient = models.ManyToManyField(
        Ingredient,
        related_name='allergies',
        blank=True
    )

    def __str__(self):
        return self.name

# for ingredients that are in a specific recipe    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )

    quantity = models.CharField(
        max_length=100,
        help_text="e.g. 2 cups, 1 tsp, 3 pieces"
    )

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name}"

# for ingredients a user has to cook with    
class UserIngredient(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} has {self.ingredient.name}"
    
