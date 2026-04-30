from urllib.parse import quote_plus

import requests
from django.conf import settings


def fetch_unsplash_image(query):
    """Return an image URL for a query using Unsplash.

    Uses the official search API when a key is configured, otherwise falls
    back to the Unsplash Source endpoint so the page still shows an image.
    """
    api_key = getattr(settings, 'UNSPLASH_API_KEY', '')
    fallback_url = f'https://source.unsplash.com/featured/?{quote_plus(query)}'

    if not api_key:
        return fallback_url

    try:
        response = requests.get(
            'https://api.unsplash.com/search/photos',
            params={
                'query': query,
                'per_page': 1,
                'client_id': api_key,
                'orientation': 'landscape',
            },
            timeout=6,
        )
        response.raise_for_status()
        data = response.json()
        if data.get('results'):
            return data['results'][0]['urls']['regular']
    except Exception:
        pass

    return fallback_url
