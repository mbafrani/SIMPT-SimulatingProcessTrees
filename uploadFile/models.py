from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
 name = models.CharField(max_length=12)
 file = models.FileField(upload_to='log')
