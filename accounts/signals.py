from users.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Account, UserDocument


@receiver(post_save, sender=CustomUser)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance,)
        UserDocument.objects.create(user=instance,)
   