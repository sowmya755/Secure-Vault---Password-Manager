import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# 🔐 PASSWORD ENTRY
class PasswordEntry(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vault_id = models.UUIDField(default=uuid.uuid4, editable=False)

    password_name = models.CharField(max_length=100)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.password_name} ({self.vault_id})"


# 🔑 USER PIN
class UserPIN(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.CharField(max_length=6)

    def __str__(self):
        return self.user.username   # ✅ FIX HERE