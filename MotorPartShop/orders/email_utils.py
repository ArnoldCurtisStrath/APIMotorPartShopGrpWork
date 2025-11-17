from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation_email(order):
    """Send order confirmation email to the customer."""
    subject = f'Order #{order.id} Confirmation - Motor Parts Shop'
    message = f"""
Dear {order.user.username},

Thank you for your order! Your order #{order.id} has been received and is being processed.

Order Details:
- Order ID: #{order.id}
- Total Amount: KSh {order.total_price}

We'll notify you once your order is ready for shipment.

Thank you for shopping with Motor Parts Shop!

Best regards,
Motor Parts Shop Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=True
    )


def send_order_status_email(order):
    """Send order status update email to the customer."""
    subject = f'Order #{order.id} Status Update - Motor Parts Shop'
    message = f"""
Dear {order.user.username},

Your order #{order.id} status has been updated.

Current Status: {order.get_status_display()}

You can track your order progress at any time through your account.

Thank you for your patience!

Best regards,
Motor Parts Shop Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=True
    )


def send_welcome_email(user):
    """Send welcome email to newly registered users."""
    subject = 'Welcome to Motor Parts Shop!'
    message = f"""
Dear {user.username},

Welcome to Motor Parts Shop!

We're thrilled to have you as part of our community. We offer a wide range of quality motor parts for all your automotive needs.

Start browsing our catalog and find the perfect parts for your vehicle. Don't hesitate to reach out if you need any assistance.

Happy shopping!

Best regards,
Motor Parts Shop Team
"""
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True
    )
