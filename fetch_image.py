#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import requests
from django.conf import settings
from catalog.models import Recipe

recipe = Recipe.objects.get(title='Garlic Butter Pasta')

api_key = settings.UNSPLASH_API_KEY
url = 'https://api.unsplash.com/search/photos'
params = {
    'query': 'garlic butter pasta',
    'per_page': 1,
    'client_id': api_key,
    'orientation': 'landscape',
}
response = requests.get(url, params=params, timeout=5)
data = response.json()

if data.get('results'):
    image_url = data['results'][0]['urls']['regular']
    recipe.image_url = image_url
    recipe.save()
    print(f'✓ Added image to Garlic Butter Pasta')
else:
    print('✗ No image found')
