from django.db import models
import datetime

# Create your models here.

YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]

class Student(models.Model):
    student_id = models.CharField(max_length=50, primary_key=True)
    student_name = models.CharField(max_length=50)
    join_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    semester = models.IntegerField()
    roll = models.IntegerField()
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.student_id + " " + self.student_name