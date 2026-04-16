import os
import json
from django.core.management.base import BaseCommand
from catalog.models import Recipe, Ingredient, RecipeIngredient, RecipeStep

# used to load recipes from json
class Command(BaseCommand):
    help = "Import recipes from JSON files"

    def add_arguments(self, parser):
        parser.add_argument(
            'directory',
            type=str,
            help='Directory containing recipe JSON files'
        )

    def handle(self, *args, **kwargs):
        directory = kwargs['directory']

        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".json"):
                    filepath = os.path.join(root, file)

                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    self.import_recipe(data)

                    self.stdout.write(self.style.SUCCESS(f"Imported {file}"))

    def import_recipe(self, data):
        recipe, _ = Recipe.objects.get_or_create(
            title=data["title"],
            defaults={
                "description": data.get("description", ""),
                "time_to_make": data["time_to_make"],
                "rating": 5,
            },
        )

        # ingredients
        for item in data["ingredients"]:
            name = item["name"].lower().strip()

            ingredient = Ingredient.objects.filter(name__iexact=name).first()
            if ingredient is None:
                ingredient = Ingredient.objects.create(name=name)

            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ingredient,
                defaults={"quantity": item["quantity"]}
            )

        # steps
        for step in data["steps"]:
            RecipeStep.objects.get_or_create(
                recipe=recipe,
                order=step["order"],
                defaults={"instruction": step["instruction"]}
            )