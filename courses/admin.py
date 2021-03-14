from django.contrib import admin
from .models import Subject
from .models import Exams
from .models import selectedcourses, studentgrades, Term, exam_application


# Register your models here.

admin.site.register(Subject)
# admin.site.register(Class)
admin.site.register(Exams)
admin.site.register(selectedcourses)
admin.site.register(studentgrades)
admin.site.register(Term)
admin.site.register(exam_application)