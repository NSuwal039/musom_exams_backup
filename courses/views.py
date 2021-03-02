from django.shortcuts import render, get_object_or_404
from teacher.models import Teacher
from .models import Subject, studentgrades
from .models import Exams
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ExamsForm, CoursesForm

# # Create your views here.

def index(request):
    return render(request, 'courses/index.html')

def addcourse(request):
    teachers = Teacher.objects.all

    if request.method == 'POST':
        formdata = CoursesForm(request.POST)
        formdata.save()
        return HttpResponseRedirect(reverse('courses:index'))
    else:
        course_form = CoursesForm
        return render(request, 'courses/addcourse.html', {'teacher': teachers, 'form':course_form})

def addexam(request):
    subjects =  Subject.objects.all
    # classes = Class.objects.all
    if request.method == 'POST':
        examinfo = ExamsForm(request.POST)
        examinfo.save()
        return HttpResponseRedirect(reverse('courses:index'))
    else:
        exam_form = ExamsForm
        return render (request, 'courses/addexam.html', {'subject': subjects, 'form':exam_form})

def examresults(request):
    exams = Exams.objects.all()
    return render(request, 'courses/publishresults.html',{'exams':exams})

def viewresults(request):
    selectedexam = get_object_or_404(Exams, exam_id = request.GET['exam'])
    results = studentgrades.objects.all().filter(exam_id = selectedexam).order_by('-marks')
    return render(request, 'courses/results.html', {'results':results, 'exam':selectedexam})
        
