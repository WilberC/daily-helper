from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Brand


class Command(BaseCommand):
    help = 'Seeds the database with common product brands'

    def handle(self, *args, **options):
        brands_data = [
            {'name': 'Coca Cola'},
            {'name': 'Pepsi'},
            {'name': 'Nestle'},
            {'name': 'Gloria'},
            {'name': 'San Luis'},
            {'name': 'Cielo'},
            {'name': 'Inka Kola'},
            {'name': 'Lay\'s'},
            {'name': 'Colgate'},
            {'name': 'Procter & Gamble'},
        ]

        with transaction.atomic():
            initial_count = Brand.objects.count()
            brands = [Brand(**data) for data in brands_data]
            Brand.objects.bulk_create(brands, ignore_conflicts=True)
            final_count = Brand.objects.count()
            
            created = final_count - initial_count
            self.stdout.write(self.style.SUCCESS(f'✓ Brands: {created} created, {len(brands_data) - created} already existed'))
