from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model inheriting from Django's AbstractUser.
    It can be extended with additional fields if needed.
    """
    pass
