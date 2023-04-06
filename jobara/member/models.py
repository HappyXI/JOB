from django.db import models

# Create your models here.
class Member(models.Model) :
    
    id = models.CharField(max_length=20, primary_key=True)
    board = models.IntegerField(null= True)
    name = models.CharField(max_length=20)
    pass1 = models.CharField(max_length=20)
    gender = models.IntegerField(default=0)
    tel = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    picture = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    address_detail = models.CharField(max_length=200)
    birthday = models.DateTimeField(null = True)
    
    #def __repr__(self) : 같은 함수
    def __str__(self):
        return self.id + ":" + self.name + ":" +self.pass1