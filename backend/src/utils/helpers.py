import re


def generate_slug(text: str) -> str:
    """Generate a URL-friendly slug from a text string."""
    # Convert to lowercase
    slug = text.lower()
    # Replace non-alphanumeric characters with hyphens
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    # Remove leading and trailing hyphens
    slug = slug.strip('-')
    return slug
