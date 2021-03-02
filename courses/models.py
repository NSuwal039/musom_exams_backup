from django.db import models
from teacher.models import Teacher
from student.models import Student

# Create your models here.

class Subject(models.Model):
    subject_code = models.CharField(max_length=50, default=None, primary_key=True)
    subject_name = models.CharField(max_length=50, default=None)
    subject_author = models.CharField(max_length=50, default=None)
    teacher_id = models.ForeignKey(Teacher, default=None, on_delete=models.CASCADE, related_name='subject_teacher')
    pass_marks = models.IntegerField(default=None)
    final_marks = models.IntegerField(default=None)

    def __str__(self):
        return self.subject_name


class Exams(models.Model):
    exam_id = models.CharField(max_length=50, default=None, primary_key=True)
    exam_title = models.CharField(max_length=50, default=None)
    exam_format = models.CharField(max_length=50, default=None)
    subject_id = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE)
    # class_id = models.ForeignKey(Class, default=None, on_delete=models.CASCADE)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    room = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.exam_title


class studentgrades(models.Model):
    student_id = models.ForeignKey(Student, default=None, on_delete=models.CASCADE, related_name='grade_student')
    exam_id = models.ForeignKey(Exams, default=None, on_delete=models.CASCADE)
    semester = models.IntegerField(default = None)
    marks = models.IntegerField(default=0)


class selectedcourses(models.Model):
    student_id = models.ForeignKey(Student, default=None, on_delete=models.CASCADE, related_name='course_student')
    subject_id = models.ForeignKey(Subject, default=None, on_delete=models.CASCADE)
    # year = models.IntegerField(default=0)
    semester = models.IntegerField(default = None)
    # class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)