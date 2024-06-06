from django.db import models
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class LicenseKey(models.Model):
    key = models.TextField(default="")
    created_time = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        return self.is_active and self.created_time + timedelta(seconds=300) > timezone.now()   #Key het han sau 300s
