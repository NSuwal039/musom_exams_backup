from django.db import models

# Create your models here.

# class Class(models.Model):
#     class_id = models.CharField(max_length=50, default=None, primary_key=True)
#     class_grade = models.CharField(max_length=50, default=None)
#     class_section = models.CharField(max_length=50, default=None)

#     def __str__(self):
#         return self.class_grade + " '" + self.class_section + "'"


class Student(models.Model):
    student_id = models.CharField(max_length=50, default=None, primary_key=True)
    student_name = models.CharField(max_length=50, default=None)
    join_year = models
    semester = models.IntegerField
    roll = models.IntegerField(default=None)
    email = models.CharField(max_length=50, default=None)

    
    def __str__(self):
        return self.student_name