from django.db import models



# Create your models here.
class Database(models.Model):
    board_num = models.IntegerField(primary_key=True)
    company_name = models.CharField(max_length=100)
    industry_classification = models.CharField(max_length=100)
    grade = models.FloatField()
    score = models.IntegerField()
    answer = models.TextField()
   

    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'
 
        
class Comtype(models.Model):
    board_num = models.IntegerField(primary_key=True)
    Thirties = models.IntegerField()
    hundred = models.IntegerField()
    big = models.IntegerField()
    public = models.IntegerField()
    foreign = models.IntegerField()
    mid = models.IntegerField()
    offering = models.IntegerField()
    kosdaq = models.IntegerField() 
   

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
    answer = models.TextField()
    
    def __str__(self):
        return str(self.board_num) + ":" + self.company_name
    class Meta:
        app_label = 'database'   


            
        
        