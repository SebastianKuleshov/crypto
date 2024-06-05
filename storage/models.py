from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from exchanges.utils import get_tokens

# Create your models here.


class Storage(models.Model):
    TOKEN = get_tokens()
    TOKEN = [(token, token) for token in TOKEN]
    token = models.CharField(max_length=100, unique=True, choices=TOKEN, default="BTC")
    count = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.token}"
