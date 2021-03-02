from django.contrib import admin
from .models import Subject
from .models import Exams
from .models import selectedcourses, studentgrades


# Register your models here.

admin.site.register(Subject)
# admin.site.register(Class)
admin.site.register(Exams)
admin.site.register(selectedcourses)
admin.site.register(studentgrades)