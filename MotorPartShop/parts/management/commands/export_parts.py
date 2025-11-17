from django.core.management.base import BaseCommand
from parts.models import Part
import csv
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Export all parts data to CSV file'

    def handle(self, *args, **kwargs):
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'exports/parts_export_{timestamp}.csv'
        
        # Export data
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Category', 'Price', 'Stock', 'In Stock', 'Created'])
            
            for part in Part.objects.select_related('category').order_by('id'):
                writer.writerow([
                    part.id,
                    part.name,
                    part.category.name,
                    part.price,
                    part.stock,
                    'Yes' if part.in_stock else 'No',
                    part.created_at.strftime('%Y-%m-%d')
                ])
        
        count = Part.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported {count} parts to {filename}')
        )