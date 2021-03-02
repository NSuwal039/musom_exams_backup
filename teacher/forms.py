from django.db.models import fields
from django.db.models.base import Model
from django.forms.models import modelform_factory
from courses.models import studentgrades
from django.forms import ModelForm

class gradesform(ModelForm):
    class Meta:
        model = studentgrades
        fields = '__all__'
        exclude=('exam_id',)  
