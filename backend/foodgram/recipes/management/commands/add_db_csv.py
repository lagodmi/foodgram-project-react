import csv
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Заполняет базу данных данными из CSV-файлов'

    def handle(self, *args, **options):
        model = Ingredient
        csv_file = 'data/ingredients.csv'

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                model.objects.get_or_create(**row)

        self.stdout.write(self.style.SUCCESS(
            'Данные из ingredients.csv успешно загружены в базу данных'
        ))
