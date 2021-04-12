from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from teacher.models import Teacher
from student.models import Student
import datetime
from django.utils import timezone

YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]

class Term(models.Model):
    term_id = models.CharField(max_length=30, primary_key=True)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    term_name = models.CharField(max_length=25)
    start_date = models.DateField()
    end_date = models.DateField()
    exam_centre = models.CharField(max_length=30)
   
    
    def get_latest(self):
        return self.latest('start_date')
    
    def __str__(self):
        return self.term_name
class Subject(models.Model):
    subject_code = models.CharField(max_length=12, primary_key=True)
    subject_name = models.CharField(max_length=25)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subject_teacher')

    def __str__(self):
        return self.subject_code + " " + self.subject_name


class Exams(models.Model):
    exam_id = models.CharField(max_length=25, primary_key=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam_title = models.CharField(max_length=25)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_format = models.CharField(max_length=6, )
    date = models.DateField()
    time = models.TimeField()
    full_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=40)

    def __str__(self):
        return  self.exam_title 

class application_form(models.Model):
    application_id = models.CharField( max_length=30,primary_key=True)
    status = models.BooleanField(max_length=3, default=False)  #False = pending
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam = models.ManyToManyField(Exams, through='studentgrades')
    semester = models.IntegerField()
    application_date = models.DateField(default=timezone.now)

    
    def save(self, *args, **kwargs):
        self.semester = self.student.semester
        super().save(*args, **kwargs)

class studentgrades(models.Model):
    exam_id = models.ForeignKey(Exams, on_delete=models.CASCADE)
    application_id = models.ForeignKey(application_form, on_delete=models.CASCADE)
    marks = models.IntegerField(default=-1)
    passed = models.BooleanField()
    exam_type = models.BooleanField() #True=Regular, False=Chance

    def __str__(self):
        return self.application_id.student.student_name + " " + self.exam_id.exam_title
    
    def save(self, *args, **kwargs):
        self.passed = True if self.marks>self.exam_id.pass_marks else False
        super().save(*args, **kwargs)

class selectedcourses(models.Model):
    student_id = models.ForeignKey(Student,  on_delete=models.CASCADE, related_name='course_student')
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    semester = models.IntegerField(default = None)

    def __str__(self):
        return self.student_id.student_name + " " + self.subject_id.subject_name