from django.core.management.base import BaseCommand
from app.models import FruitFarmingOption

class Command(BaseCommand):
    help = 'Populate Fruit Farming Options in the database'

    def handle(self, *args, **options):
        options_data = [
            {
                "title": "PinaApple Farming",
                "invest_amount": 4899,
                "earn_amount": 26969,
                "per_day_earn": 899,
                "days": 30,
                "icon": "fas fa-apple",
                "description": "Description of PinaApple Farming.",
            },
            {
                "title": "Pears Farming",
                "invest_amount": 8599,
                "earn_amount": 46350,
                "per_day_earn": 1545,
                "days": 30,
                "icon": "fas fa-pear",
                "description": "Description of Pears Farming.",
            },
            {
                "title": "Orange Farming",
                "invest_amount": 13899,
                "earn_amount": 88470,
                "per_day_earn": 2949,
                "days": 30,
                "icon": "fas fa-orange",
                "description": "Description of Orange Farming.",
            },
            {
                "title": "Mango Farming",
                "invest_amount": 20999,
                "earn_amount": 107970,
                "per_day_earn": 3599,
                "days": 30,
                "icon": "fas fa-mango",
                "description": "Description of Mango Farming.",
            },
            {
                "title": "Watermelon Farming",
                "invest_amount": 28999,
                "earn_amount": 138750,
                "per_day_earn": 4625,
                "days": 30,
                "icon": "fas fa-watermelon",
                "description": "Description of Watermelon Farming.",
            }, 
            {
                "title": "Apple Farming",
                "invest_amount": 546,
                "earn_amount": 2040,
                "per_day_earn": 85,
                "days": 30,
                "icon": "fas fa-apple",
                "description": "Description of Apple Farming.",
            },
            {
                "title": "Guava Farming",
                "invest_amount": 2685,
                "earn_amount": 14670,
                "per_day_earn": 489,
                "days": 30,
                "icon": "fas fa-leaf",
                "description": "Description of Guava Farming.",
            },
        ]


        options_to_create = [
            FruitFarmingOption(**option_data) for option_data in options_data
        ]
        FruitFarmingOption.objects.bulk_create(options_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
