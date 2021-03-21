from django.db import models
from django.db.models.deletion import CASCADE
from teacher.models import Teacher
from student.models import Student
import datetime

# Create your models here.
YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]
EXAM_CHOICES = [("REG","Regular"),
                ("CHA","Chance")]
# TERM_CHOICES=[("MID", "Mid Term"), ("FIN","Final Term")]
# FORM_STATUS =   [("APL", "Applied"),
#                 ("PEN", "Pending"),
#                 ("REG", "Registered")]

class Term(models.Model):
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    exam_name = models.CharField(max_length=25)
    Start_date = models.DateField()
    End_date = models.DateField()
   
    def __str__(self):
       return self.exam_name

class Subject(models.Model):
    subject_code = models.CharField(max_length=12, primary_key=True)
    subject_name = models.CharField(max_length=25)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='subject_teacher')

    def __str__(self):
        return self.subject_code + " " + self.subject_name


class Exams(models.Model):
    exam_id = models.CharField(max_length=25, primary_key=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam_title = models.CharField(max_length=25, )
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_format = models.CharField(max_length=6, )
    date = models.DateField()
    time = models.TimeField()
    full_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=40)
    exam_centre = models.CharField(max_length=30, )

    def __str__(self):
        return  self.exam_title 

class application_form(models.Model):
    application_id = models.CharField( max_length=30,primary_key=True)
    status = models.BooleanField(max_length=3, default=False)  #False = pending
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam = models.ManyToManyField(Exams, through='studentgrades')
    semester = models.IntegerField()
    application_date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.student.student_name + " " + self.exam.exam_title
    
    def save(self, *args, **kwargs):
        self.semester = self.student.semester
        super().save(*args, **kwargs)

class studentgrades(models.Model):
    exam_id = models.ForeignKey(Exams, on_delete=models.CASCADE)
    application_id = models.ForeignKey(application_form, on_delete=models.CASCADE)
    marks = models.IntegerField()
    passed = models.BooleanField()
    exam_type = models.CharField(
        max_length=10,
        choices=EXAM_CHOICES
    )

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