from django.core.management.base import BaseCommand
from orders.models import Order
import csv
import os
from datetime import datetime

class Command(BaseCommand):
    help = 'Export all orders data to CSV file'

    def handle(self, *args, **kwargs):
        # Create exports directory if it doesn't exist
        os.makedirs('exports', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'exports/orders_export_{timestamp}.csv'
        
        # Export data
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Order ID', 'Username', 'Email', 'Status', 'Total Price', 'Items Count', 'Order Date'])
            
            for order in Order.objects.select_related('user').prefetch_related('items').order_by('-created_at'):
                writer.writerow([
                    order.id,
                    order.user.username,
                    order.user.email,
                    order.get_status_display(),
                    order.total_price,
                    order.items.count(),
                    order.created_at.strftime('%Y-%m-%d %H:%M')
                ])
        
        count = Order.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported {count} orders to {filename}')
        )