import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Skill


class Command(BaseCommand):
    help = "Add Unsplash images to skills"

    def fetch_unsplash_image(self, query):
        api_key = getattr(settings, "UNSPLASH_API_KEY", None)
        if not api_key:
            return None

        try:
            url = "https://api.unsplash.com/search/photos"
            params = {
                "query": query,
                "per_page": 1,
                "client_id": api_key,
                "orientation": "landscape",
            }

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("results"):
                return data["results"][0]["urls"]["regular"]

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"Image error for {query}: {e}"))

        return None

    def handle(self, *args, **kwargs):
        skills = Skill.objects.all()

        for skill in skills:
            if skill.image_url:
                self.stdout.write(f"Skipping {skill.name}, already has image")
                continue

            image_url = self.fetch_unsplash_image(skill.name)

            if image_url:
                skill.image_url = image_url
                skill.save()
                self.stdout.write(self.style.SUCCESS(f"Added image for {skill.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"No image found for {skill.name}"))