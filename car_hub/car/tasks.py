import os
import sys

from celery import shared_task
from django.utils.translation import gettext as _

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client.models import Client
from config import email_host_user
from django.core.mail import send_mail

from .models import Car


@shared_task
def send_inform_text(user_id, car_id, total_price ):
    try:
        client = Client.objects.get(user_id=user_id)
        car = Car.objects.get(id=car_id)

        send_mail(
            subject='Purchase Confirmation',
            message=(
                f'Dear {client.user.username},\n\n'
                f'You have successfully completed the purchase of "{car.brand} {car.model}".\n'
                f'Total price: {total_price}\n'
                'Our manager will contact you shortly.\n\nThank you for choosing us!'
            ),
            from_email=email_host_user,
            recipient_list=[client.email],
            fail_silently=False,
        )
        print("Thank you for your purchase, we sent you an email")
    except Client.DoesNotExist:
        print("Client not found. Email not sent.")
    except Car.DoesNotExist:
        print("Car not found. Email not sent.")