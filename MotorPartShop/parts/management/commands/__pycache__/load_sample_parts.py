from django.core.management.base import BaseCommand
from parts.models import Category, Part

class Command(BaseCommand):
    help = 'Load sample parts data'
    
    def handle(self, *args, **kwargs):
        # Create categories
        engine = Category.objects.create(name='Engine Parts', description='Engine related components')
        brake = Category.objects.create(name='Brake System', description='Brake components')
        electrical = Category.objects.create(name='Electrical', description='Electrical components')
        
        # Create parts
        Part.objects.create(
            name='Engine Oil Filter',
            category=engine,
            description='High-quality oil filter for most engines',
            price=1599.00,
            stock=50
        )
        Part.objects.create(
            name='Brake Pads',
            category=brake,
            description='Front brake pads - universal fit',
            price=4550.00,
            stock=30
        )
        Part.objects.create(
            name='Air Filter',
            category=engine,
            description='Performance air filter',
            price=1275.00,
            stock=40
        )
        Part.objects.create(
            name='Spark Plugs',
            category=electrical,
            description='Set of 4 spark plugs',
            price=899.00,
            stock=100
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded sample parts'))
