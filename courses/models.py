from django.db import models
from teacher.models import Teacher
from student.models import Student
import datetime

# Create your models here.
YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]

class Subject(models.Model):
    subject_code = models.CharField(max_length=50, default=None, primary_key=True)
    subject_name = models.CharField(max_length=50, default=None)
    subject_author = models.CharField(max_length=50, default=None)
    teacher_id = models.ForeignKey(Teacher, default=None, on_delete=models.CASCADE, related_name='subject_teacher')
    pass_marks = models.IntegerField(default=None)
    final_marks = models.IntegerField(default=None)

    def __str__(self):
        return self.subject_code + " " + self.subject_name


class Exams(models.Model):
    exam_id = models.CharField(max_length=50, default=None, primary_key=True)
    exam_title = models.CharField(max_length=50, default=None)
    exam_format = models.CharField(max_length=50, default=None)
    subject_id = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE)
    term = models.CharField(
        max_length=16,
       choices=[("MID", "Mid Term"), ("FIN","Final Term")],  
   )
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    room = models.CharField(max_length=50, default=None)

    def __str__(self):
        return  self.exam_title 


class studentgrades(models.Model):
    student_id = models.ForeignKey(Student, default=None, on_delete=models.CASCADE, related_name='grade_student')
    exam_id = models.ForeignKey(Exams, default=None, on_delete=models.CASCADE)
    semester = models.IntegerField(default = None)
    marks = models.IntegerField(default=0)

    def __str__(self):
        return self.student_id.student_name + " " + self.exam_id.exam_title


class selectedcourses(models.Model):
    student_id = models.ForeignKey(Student, default=None, on_delete=models.CASCADE, related_name='course_student')
    subject_id = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    semester = models.IntegerField(default = None)