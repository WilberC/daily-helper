from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Master seed command to run all data seeders in the correct order'

    def add_arguments(self, parser):
        parser.add_argument(
            '--only',
            type=str,
            help='Run only a specific seed command (e.g., --only seed_products)',
        )

    def handle(self, *args, **options):
        # Define the order of seeds to handle dependencies correctly
        # 1. Reference Data (Categories, Units, Presentations)
        # 2. Brands
        # 3. Products/Variants (coming soon)
        all_seeds = [
            'seed_products',
            'seed_brands',
        ]

        # Filter if --only is provided
        if options['only']:
            seeds_to_run = [options['only']]
        else:
            seeds_to_run = all_seeds

        self.stdout.write(self.style.MIGRATE_HEADING("--- Starting Database Seeding ---"))

        for seed_cmd in seeds_to_run:
            self.stdout.write(f"\n[Running: {seed_cmd}]")
            try:
                call_command(seed_cmd)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error in {seed_cmd}: {e}"))
                self.stdout.write(self.style.WARNING("Stopping seed process due to error."))
                return

        self.stdout.write(self.style.SUCCESS("\n✓ Master seed process completed!"))
