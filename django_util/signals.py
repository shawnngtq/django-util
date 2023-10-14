import logging

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    This receiver signal creates Profile object when User object is saved

    Reference
    ---------
    - https://docs.djangoproject.com/en/dev/topics/signals/#receiver-functions
    - https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
