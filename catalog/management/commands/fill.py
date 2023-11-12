from django.core.management import BaseCommand
from catalog.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        data = Category.objects.all()
        data.delete()
        category_list = [
            {'name': 'Парсер данных', 'description': 'Код предназначенный для агрегации и сбора данных с сайтов'},
            {'name': 'Сервис рассылок', 'description': 'Код позволяющий установить сервис рассылок на ваш сервер'},
        ]

        for category_item in category_list:
            Category.objects.create(**category_item)
