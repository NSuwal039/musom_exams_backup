from django.contrib import messages 
from django.shortcuts import redirect, render, get_object_or_404
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
    course_form = CoursesForm

    if request.method == 'POST':
        formdata = CoursesForm(request.POST)
        if formdata.is_valid():
            formdata.save()
            return HttpResponseRedirect(reverse('courses:index'))
        else:
            messages.error(request, "Course info invalid. Please check your information and try again.")
            return render( request, 'courses/addcourse.html', {'form':course_form})
    else:
        return render(request, 'courses/addcourse.html', {'teacher': teachers, 'form':course_form})

def addexam(request):
    subjects =  Subject.objects.all
    # classes = Class.objects.all
    exam_form = ExamsForm
    if request.method == 'POST':
        examinfo = ExamsForm(request.POST)
        if examinfo.is_valid():
            examinfo.save()
            return HttpResponseRedirect(reverse('courses:index'))
        else:
            messages.error(request, "Exam info invalid. Please check your information and try again.")
            return render( request, 'courses/addexam.html', {'form':exam_form})
    else:
        return render (request, 'courses/addexam.html', {'subject': subjects, 'form':exam_form})

def examresults(request):
    exams = Exams.objects.all()
    return render(request, 'courses/publishresults.html',{'exams':exams})

def viewresults(request):
    selectedexam = get_object_or_404(Exams, exam_id = request.GET['exam'])
    results = studentgrades.objects.all().filter(exam_id = selectedexam).order_by('-marks')
    return render(request, 'courses/results.html', {'results':results, 'exam':selectedexam})

def subjectAjax(request):
    pass

def termAjax(request):
    pass

def yearAjax(request):
    pass
        
