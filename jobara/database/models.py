from django.db import models

# Create your models here.
class Database(models.Model):
    board_num = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=100)
    industry_classification = models.CharField(max_length=100)
    grade = models.FloatField()
    score = models.IntegerField()
    answer = models.CharField(max_length=10000)
   

    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'
        
        
class companydetail(models.Model):
    ccode = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'
        
        
        
class company(models.Model):
    ccode = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'
        
        
class jobdetail(models.Model):
    jcode = models.IntegerField(primary_key=True)
    industry_classification = models.CharField(max_length=100)

    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'
        
        

class job(models.Model):
    jcode = models.IntegerField(primary_key=True)
    industry_name = models.CharField(max_length=100)
    
    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'        
        
        
class resume(models.Model):
    key = models.AutoField(primary_key=True)
    ccode = models.IntegerField()
    jcode = models.IntegerField()
    answer = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'   


class good(models.Model):
    index = models.AutoField(primary_key=True)
    key = models.IntegerField()
    ccode = models.IntegerField()
    jcode = models.IntegerField()
    value = models.CharField(max_length=20)
     
    
    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'   
        
        
        
        