from django.db.models.signals import post_save
from django.dispatch import receiver

from .email_utils import send_order_confirmation_email, send_order_status_email
from .models import Order


@receiver(post_save, sender=Order)
def order_notification(sender, instance, created, **kwargs):
    """Signal handler to send email notifications for order creation and updates."""
    if created:
        # New order created - send confirmation email
        send_order_confirmation_email(instance)
    else:
        # Order updated - send status update email
        send_order_status_email(instance)

