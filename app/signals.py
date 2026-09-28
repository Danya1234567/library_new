from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Employee

@receiver(post_save, sender=Employee)
def sync_default_group(sender, instance, created, **kwargs):
    if created and instance.position.default_group:
        instance.user.groups.add(instance.position.default_group)