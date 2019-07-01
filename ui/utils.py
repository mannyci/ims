from django.contrib.auth import get_user_model


def needs_setup():
    return not get_user_model().objects.all().exists()
