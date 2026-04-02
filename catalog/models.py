import uuid
from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint # Constrains fields to unique values
from django.db.models.functions import Lower # Returns lower cased value of field

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

    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        null=True
    )

    tool = models.ForeignKey(
        Tool,
        on_delete=models.SET_NULL,
        null=True
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.SET_NULL,
        null=True
    )

    steps = models.TextField()
    time_to_make = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])


class Allergy(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter an Allergy(e.g. nuts, berries etc.)"
    )

    Ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.name
