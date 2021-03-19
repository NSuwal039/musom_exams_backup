from django.db import models
from .models import Subject, Exams
from django.forms import ModelForm, fields
from django import forms

class CoursesForm(ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        

class ExamsForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ExamsForm, self).__init__(*args, **kwargs)
        self.fields['exam_title'].widget.attrs['readonly'] = True
        self.fields['exam_id'].widget.attrs['readonly'] = True
        
        
    class Meta:
        model = Exams
        fields = '__all__'