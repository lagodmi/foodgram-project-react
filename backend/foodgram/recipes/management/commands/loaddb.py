from django.core.management.base import BaseCommand
import json

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Populates the ingredients table from ingredients.json'

    def handle(self, *args, **options):
        with open('data/ingredients.json', 'r', encoding='utf-8') as file:
            reader = json.load(file)
            for row in reader:
                Ingredient.objects.update_or_create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
        self.stdout.write(self.style.SUCCESS(
            'Data from ingredients.json loaded successfully'
        ))
