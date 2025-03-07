from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return f"Name: {self.name} - email :{self.email}"
