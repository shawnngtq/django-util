def create_user_profile(sender, instance, created, profile_object, **kwargs):
    """
    This receiver signal creates Profile object when User object is saved

    Reference
    ---------
    - https://docs.djangoproject.com/en/dev/topics/signals/#receiver-functions
    - https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    """
    if created:
        profile_object.objects.create(user=instance)
