from django.db import models
from django.contrib.auth.models import AbstractUser

class Book(models.Model):
    title = models.CharField(max_length=70)
    author = models.CharField(max_length=30)
    published_date = models.DateField()
    isbn = models.CharField()
    
    def __str__(self):
        return self.title
    
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_premium = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Create your models here.
