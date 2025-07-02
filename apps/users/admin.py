from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """We inherit from the base UserAdmin to leverage all its functionality"""
    pass
