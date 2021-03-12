from django.db import models

# Create your models here.

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=50, primary_key=True)
    teacher_name = models.CharField(max_length=50)
    #photo = models.ImageField(upload_to='pics/teacher')
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.teacher_name