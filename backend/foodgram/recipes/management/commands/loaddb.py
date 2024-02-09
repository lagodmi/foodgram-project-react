from django.core.management.base import BaseCommand
import json

from recipes.models import Ingredient, Tag

LIST_TAG = [
    {'name': 'завтрак', 'color': '#FF0000', 'slug': 'breakfast'},
    {'name': 'обед', 'color': '#1100FF', 'slug': 'lunch'},
    {'name': 'ужин', 'color': '#11FF11', 'slug': 'dinner'},
]


class Command(BaseCommand):
    help = 'Populates the ingredients table from ingredients.json'

    def handle(self, *args, **options):
        with open('data/ingredients.json', 'r', encoding='utf-8') as file:
            reader = json.load(file)
            for row in reader:
                Ingredient.objects.create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
        self.stdout.write(self.style.SUCCESS(
            'Data from ingredients.json loaded successfully'
        ))

        for row in LIST_TAG:
            Tag.objects.create(
                name=row['name'],
                color=row['color'],
                slug=row['slug']
            )
        self.stdout.write(self.style.SUCCESS(
            'Test data for tag loaded'
        ))
