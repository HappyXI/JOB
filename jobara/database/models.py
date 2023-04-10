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