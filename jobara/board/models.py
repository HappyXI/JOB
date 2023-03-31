from django.db import models

# Create your models here.
class Board(models.Model):
     
    content= models.CharField(max_length=5000)
     

def __str__(self):
    return str(self.num) + ":" + self.subject