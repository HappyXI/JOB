from django.db import models

# Create your models here.
class Board(models.Model):
    
    num = models.AutoField(primary_key=True)
    id = models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=100)
    content = models.CharField(max_length=5000)
    regdate = models.DateTimeField(null = True) #null 허용
    readcnt = models.IntegerField(default = 0)
    file1 = models.CharField(max_length=300)
     
    def __str__(self):
        return str(self.num) + ":" + self.subject
