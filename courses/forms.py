from django.db import models
from .models import Subject, Exams
from django.forms import ModelForm, fields

class CoursesForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        

class ExamsForm(ModelForm):
    class Meta:
        model = Exams
        fields = '__all__'