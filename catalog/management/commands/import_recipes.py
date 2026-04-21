import os
import json
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
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

    def fetch_unsplash_image(self, query):
        """Fetch recipe image URL from Unsplash API"""
        api_key = getattr(settings, 'UNSPLASH_API_KEY', None)
        if not api_key:
            return None
        
        try:
            url = 'https://api.unsplash.com/search/photos'
            params = {
                'query': query,
                'per_page': 1,
                'client_id': api_key,
                'orientation': 'landscape',
            }
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data.get('results'):
                image_url = data['results'][0]['urls']['regular']
                self.stdout.write(self.style.SUCCESS(f"✓ Image found for '{query}'"))
                return image_url
            else:
                # tries a stupid search if a good pic isnt found
                simplified = ' '.join(query.split()[:3])
                if simplified != query:
                    self.stdout.write(self.style.WARNING(f"✗ No exact match for '{query}', trying '{simplified}'..."))
                    params['query'] = simplified
                    response = requests.get(url, params=params, timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    if data.get('results'):
                        image_url = data['results'][0]['urls']['regular']
                        self.stdout.write(self.style.SUCCESS(f"✓ Found simplified image for '{query}'"))
                        return image_url
                
                self.stdout.write(self.style.WARNING(f"✗ No image found for '{query}'"))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f"✗ API error for '{query}': {e}"))
        
        return None

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
        image_url = self.fetch_unsplash_image(data["title"])
        recipe, created = Recipe.objects.get_or_create(
            title=data["title"],
            defaults={
                "description": data.get("description", ""),
                "time_to_make": data["time_to_make"],
                "rating": 5,
                "image_url": image_url,
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