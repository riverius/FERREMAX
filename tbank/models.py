from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class Usuario(AbstractUser):
    ROLES = (
        ('administrador', 'Administrador'),
        ('contador', 'Contador'),
        ('cliente', 'Cliente'),
        ('bodeguero', 'Bodeguero'),
        ('vendedor', 'Vendedor'),
    )
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',  # Custom related_name to avoid clash
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_user_permissions_set',  # Custom related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )