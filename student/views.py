from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from student.models import Student
from courses.models import Exams, studentgrades, Subject, selectedcourses
from django.urls import reverse

# # Create your views here.

# """ 
# def login(request):
#     if request.method == 'GET':
#         return render(request, 'student/login.html')
#     else:
#         student_get = get_object_or_404(Student, student_id = request.POST['userID'])
#         return render(request, 'student/index2.html', {'student': student_get})
#  """

stu_id = 'Stu_0001'
student = get_object_or_404(Student, student_id = stu_id)

def index(request):
    
    return render(request, 'student/index.html', {'student':student})

def checkscore(request):
    grades = studentgrades.objects.all().filter(student_id=student).exclude(marks=-1)
    remaining = studentgrades.objects.all().filter(student_id=student).filter(marks=-1)
    return render(request, 'student/checkscore.html', {'student': student, 'grades':grades, 'remaining':remaining})

def addcourse(request):
    if request.method == 'GET':
        courses_remove = selectedcourses.objects.all().filter(student_id=student)
        subject_list = Subject.objects.all()
        for course in courses_remove:
            subject_list = subject_list.exclude(subject_code=course.subject_id.subject_code)

        return render(request, 'student/addcourse.html', {'student':student, 'courses':subject_list})
    else:
        course_object = get_object_or_404(Subject, subject_code = request.POST['course'])
        student_object = student

        to_add = selectedcourses (subject_id=course_object, student_id=student_object, year = 1)
        to_add.save()
        message = "Course selection successful."
        return HttpResponseRedirect(reverse('student:viewcourses'))

def registerexam(request):
    if request.method == 'GET':
        courses = selectedcourses.objects.all().filter(student_id = student)
        exam = Exams.objects.all()
        returnobject = Exams.objects.none()
        for course in courses:
            exam_toadd = exam.filter(subject_id = course.subject_id)
            returnobject = returnobject|exam_toadd
        
        removeexams = studentgrades.objects.all().filter(student_id = student)
        for exams in removeexams:
            returnobject = returnobject.exclude(exam_id = exams.exam_id.exam_id)
        return render(request, 'student/registerexam.html', {'exam':returnobject, 'student':student})
    else:
        examid = request.POST['exam']
        exam=get_object_or_404(Exams, exam_id=examid)
        objectdata = studentgrades(student_id = student, exam_id = exam, marks = -1)
        objectdata.save()
        return HttpResponseRedirect(reverse('student:examdetails'))
    
def examdetails(request):
    exams = studentgrades.objects.all().filter(student_id = student)
    # to_send = Exams.objects.all().filter(exam_id__in = exams)
    return render(request, 'student/examdetails.html', {'student':student, 'exams':exams})

def viewcourses(request):
    courses = selectedcourses.objects.all().filter(student_id = student)
    return render (request, 'student/viewcourses.html', {'courses':courses, 'student':student})
