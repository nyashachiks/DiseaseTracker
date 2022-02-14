from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Practitioner


@receiver(post_save, sender=User)
def create_practitioner(sender, instance, created, **kwargs):
    if created:
        Practitioner.objects.create(practitioner=instance)


@receiver(post_save, sender=User)
def save_practitioner(sender, instance, **kwargs):
    instance.practitioner.save()