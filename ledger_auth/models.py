from django.db import models
from django.utils import timezone


class RevokedToken(models.Model):
    token = models.CharField(max_length=2024, primary_key=True, blank=False)
    exp = models.DateTimeField(blank=False)

    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
