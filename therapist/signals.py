from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Therapist
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Therapist)
def therapist_created(sender, instance, created, **kwargs):
    if created:
        print('A new user was created:', instance.name, instance.email)
        message = "Your application is currently being reviewed and will undergo processing within 15 days. You will receive an email notification regarding the status of your application, whether it has been accepted or rejected, within the specified timeframe of 15 days."

        send_mail(
            "Application to Inhealin successfully submitted",
            message, 
            'settings.EMAIL_HOST_USER',
            [instance.email]
        )

