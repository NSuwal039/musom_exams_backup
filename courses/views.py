from django.http.response import HttpResponse
from student.models import Student
from django.contrib import messages 
from django.shortcuts import redirect, render, get_object_or_404
from teacher.models import Teacher
from .models import Subject, selectedcourses, studentgrades
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

def examtoppers(request):
    exams = Exams.objects.all()
    if request.method=='GET':
        return render(request,'courses/examtoppers.html', {'exams':exams})
    else:
        selected_exam = get_object_or_404(Exams, exam_id=request.POST['exam_id'])
        studentrecords = studentgrades.objects.all().filter(exam_id=selected_exam).exclude(marks=-1).order_by('-marks')[0:3]
        selected_object = request.POST['exam_id']
        return render(request, 'courses/examtoppers.html', {'students':studentrecords, 'exams':exams, 'selected_exam':selected_exam})

def addstudentmarks(request):
    return render(request, 'courses/addstudentmarks.html')

def studentsAjax(request):
    student_id = request.GET.get("student_id")
    student_list =[]
    student_all = Student.objects.all()

    for student in student_all:
        if student_id in student.student_id:
            student_list.append(student)
    
    return render(request, 'courses/studentlist.html',{'students':student_list})

def studentsmarksentry(request, id):
    student = get_object_or_404(Student, student_id=id)
    exams = studentgrades.objects.filter(student_id = student)
    return render(request, 'courses/studentmarksentry.html', {'student': student, 'exams':exams})

def submitscores(request):
    student = get_object_or_404(Student, student_id=request.POST['student_id'])
    exams = studentgrades.objects.filter(student_id=student)

    for exam in exams:
        student_object = student
        exam_object = exam.exam_id
        marks = request.POST[exam.exam_id.exam_title]
        test = studentgrades.objects.all().filter(student_id=student_object, exam_id= exam_object)
        if test.exists():
            editobject = studentgrades.objects.get(student_id=student_object, exam_id= exam_object)
            if request.POST[exam.exam_id.exam_title]:
                editobject.marks=marks
            else:
                pass
            editobject.save()
        else:
            if request.POST[exam.exam_id.exam_title]:
                marks=marks
            else:
                marks=0        
            exam_marks = studentgrades( student_id=student_object, exam_id=exam_object, marks=marks)
            exam_marks.save()

    return HttpResponseRedirect(reverse('courses:index'))
        
