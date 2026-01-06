from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Category, UnitOfMeasure, Presentation


class Command(BaseCommand):
    help = 'Seeds the database with initial Category, UnitOfMeasure, and Presentation data'

    def handle(self, *args, **options):
        with transaction.atomic():
            self.seed_categories()
            self.seed_units_of_measure()
            self.seed_presentations()

        self.stdout.write(self.style.SUCCESS('✓ Seed completed successfully!'))

    def seed_categories(self):
        """Seed product categories with predefined colors."""
        categories_data = [
            {'name': 'Beverages', 'color': '#3B82F6'},        # Blue
            {'name': 'Dairy', 'color': '#F59E0B'},            # Amber
            {'name': 'Snacks', 'color': '#EF4444'},           # Red
            {'name': 'Cleaning', 'color': '#10B981'},         # Green
            {'name': 'Personal Care', 'color': '#8B5CF6'},    # Purple
            {'name': 'Frozen Foods', 'color': '#06B6D4'},     # Cyan
            {'name': 'Canned Goods', 'color': '#F97316'},     # Orange
            {'name': 'Bakery', 'color': '#EC4899'},           # Pink
            {'name': 'Meat & Poultry', 'color': '#DC2626'},   # Dark Red
            {'name': 'Condiments', 'color': '#84CC16'},       # Lime
            {'name': 'Grains & Cereals', 'color': '#A78BFA'}, # Light Purple
            {'name': 'Health & Wellness', 'color': '#14B8A6'},# Teal
        ]

        initial_count = Category.objects.count()
        categories = [Category(**data) for data in categories_data]
        Category.objects.bulk_create(categories, ignore_conflicts=True)
        final_count = Category.objects.count()
        
        created = final_count - initial_count
        self.stdout.write(f'  Categories: {created} created, {len(categories_data) - created} already existed')

    def seed_units_of_measure(self):
        """Seed common units of measure."""
        units_data = [
            # Volume
            {'name': 'Milliliter', 'abbreviation': 'ml'},
            {'name': 'Liter', 'abbreviation': 'L'},
            {'name': 'Fluid Ounce', 'abbreviation': 'fl oz'},
            {'name': 'Gallon', 'abbreviation': 'gal'},
            # Weight
            {'name': 'Gram', 'abbreviation': 'g'},
            {'name': 'Kilogram', 'abbreviation': 'kg'},
            {'name': 'Ounce', 'abbreviation': 'oz'},
            {'name': 'Pound', 'abbreviation': 'lb'},
            # Count
            {'name': 'Unit', 'abbreviation': 'u'},
            {'name': 'Pack', 'abbreviation': 'pk'},
            {'name': 'Dozen', 'abbreviation': 'dz'},
            {'name': 'Box', 'abbreviation': 'box'},
            # Other
            {'name': 'Piece', 'abbreviation': 'pc'},
            {'name': 'Roll', 'abbreviation': 'roll'},
            {'name': 'Sheet', 'abbreviation': 'sht'},
        ]

        initial_count = UnitOfMeasure.objects.count()
        units = [UnitOfMeasure(**data) for data in units_data]
        UnitOfMeasure.objects.bulk_create(units, ignore_conflicts=True)
        final_count = UnitOfMeasure.objects.count()
        
        created = final_count - initial_count
        self.stdout.write(f'  Units of Measure: {created} created, {len(units_data) - created} already existed')

    def seed_presentations(self):
        """Seed common product presentation types."""
        presentations_data = [
            # Bottles
            {'name': 'Plastic Bottle', 'description': 'Standard plastic container, typically PET or HDPE'},
            {'name': 'Glass Bottle', 'description': 'Glass container, often used for premium products'},
            {'name': 'Squeeze Bottle', 'description': 'Flexible plastic bottle with squeezable sides'},
            # Cartons & Boxes
            {'name': 'Tetra Pak', 'description': 'Aseptic carton packaging, commonly used for milk and juices'},
            {'name': 'Carton', 'description': 'Cardboard box packaging'},
            {'name': 'Box', 'description': 'Standard box container'},
            # Cans
            {'name': 'Aluminum Can', 'description': 'Metal can, typically for beverages'},
            {'name': 'Tin Can', 'description': 'Metal can for preserved foods'},
            # Bags & Pouches
            {'name': 'Plastic Bag', 'description': 'Flexible plastic packaging'},
            {'name': 'Paper Bag', 'description': 'Eco-friendly paper packaging'},
            {'name': 'Pouch', 'description': 'Stand-up or flat flexible pouch'},
            {'name': 'Sachet', 'description': 'Small single-use packet'},
            # Jars & Containers
            {'name': 'Glass Jar', 'description': 'Glass container with lid'},
            {'name': 'Plastic Jar', 'description': 'Plastic container with lid'},
            {'name': 'Tub', 'description': 'Wide-mouth plastic container'},
            # Large Containers
            {'name': 'Vidon', 'description': 'Large water container (typically 20L)'},
            {'name': 'Gallon Jug', 'description': 'Large plastic jug container'},
            {'name': 'Drum', 'description': 'Industrial-size container'},
            # Wrapping
            {'name': 'Wrap', 'description': 'Plastic or paper wrapping'},
            {'name': 'Blister Pack', 'description': 'Plastic packaging with cardboard backing'},
            # Other
            {'name': 'Tube', 'description': 'Squeezable tube container'},
            {'name': 'Spray Bottle', 'description': 'Container with spray mechanism'},
            {'name': 'Dispenser', 'description': 'Container with pump or dispenser mechanism'},
            {'name': 'Bulk', 'description': 'Unpackaged, sold by weight or volume'},
        ]

        initial_count = Presentation.objects.count()
        presentations = [Presentation(**data) for data in presentations_data]
        Presentation.objects.bulk_create(presentations, ignore_conflicts=True)
        final_count = Presentation.objects.count()
        
        created = final_count - initial_count
        self.stdout.write(f'  Presentations: {created} created, {len(presentations_data) - created} already existed')
