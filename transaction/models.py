from django.db import models
from django.contrib.auth import get_user_model
from storage.models import Storage

User = get_user_model()

# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.ForeignKey(Storage, on_delete=models.CASCADE)
    count = models.FloatField()
    accepted = models.BooleanField(default=None, null=True)
