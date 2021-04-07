import datetime
from datetime import datetime as date1
import json
from typing import ContextManager
from django.db.models import fields
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from student.models import Student
from courses.models import Exams, application_form, studentgrades, Subject, selectedcourses, Term
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.utils.html import format_html


student = Student.objects.none()

def index(request):
    if request.method == 'POST':
        request.session['user_id'] = request.POST['userID']
        print(request.POST['userID'])
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    print(request.META.get('HTTP_REFERER'))
    return render(request, 'student/index.html', {'student':student})

def checkscore(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    print(student)
    grades = studentgrades.objects.all().filter(application_id__student_id=student).exclude(marks=-1)
    remaining = studentgrades.objects.all().filter(application_id__student_id=student).filter(marks=-1)
    SEM_CHOICES = [(r) for r in range(1, student.semester+1)]
    return render(request, 'student/checkscore.html', {'student': student, 'grades':grades, 'remaining':remaining, 'semesters':SEM_CHOICES})

def addcourse(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    
    courses_remove = selectedcourses.objects.all().filter(student_id=student)
    subject_list = Subject.objects.all()
    for course in courses_remove:
        subject_list = subject_list.exclude(subject_code=course.subject_id.subject_code)

    return render(request, 'student/addcourse.html', {'student':student, 'courses':subject_list})

def registerexam(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
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
        objectdata = studentgrades(student_id = student, exam_id = exam, marks = -1, semester = student.semester)
        objectdata.save()
        messages.success(request, 'Exam ' + exam.exam_title + ' register successful.')
        return HttpResponseRedirect(reverse('student:index'))

def examapplication(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    terms = Term.objects.all()
    
    today = datetime.date.today()
    term=Term.objects.none()
    for term_obj in terms:
        if (datetime.timedelta(0)<=term_obj.start_date-today<=datetime.timedelta(15)):
            # print(term_obj.start_date-today)
            # print(type(term_obj.start_date-today))
            print(term_obj.__str__() + ": Yes\n")
            term=term_obj
        else:
            # print(term_obj.start_date-today)
            print(term_obj.__str__() + ": No\n")
    
    if(term):
        selected_subjects= selectedcourses.objects.filter(Q(student_id=student)&Q(semester=student.semester))
        print(selected_subjects)
        exams=[]

        for subject in selected_subjects:
            try:
                exams.append(Exams.objects.get(Q(term=term)&Q(subject_id=subject.subject_id)))
            except:
                print(subject.__str__() + " exam not found")
        print(exams)
    else:
        print("nothing")

    return render(request, 'student/examapplication.html', {'student':student, 'term':term, 'exams':exams})

def examslist(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    term_id = request.GET.get('term_id')
    term = get_object_or_404(Term, pk=term_id)
    selected_subjects=selectedcourses.objects.filter(student_id=student)
    exams = Exams.objects.filter(term = term)
    exams_list=[]

    for subject in selected_subjects:
        exam_item = exams.filter(subject_id=subject.subject_id)
        if exam_item.exists():
            exams_list.append(exam_item.last())
   
    return render(request, 'student/examslist.html', {'exams':exams_list, 'term':term})
    
def examdetails(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    exams = studentgrades.objects.all().filter(application_id__student_id = student)
    SEM_CHOICES = [(r) for r in range(1, student.semester+1)]
    # to_send = Exams.objects.all().filter(exam_id__in = exams)
    return render(request, 'student/examdetails.html', {'student':student, 'exams':exams, 'semesters':SEM_CHOICES})

def viewcourses(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    SEM_CHOICES = [(r) for r in range(1, student.semester+1)]
    courses = selectedcourses.objects.all().filter(student_id = student)
    return render (request, 'student/viewcourses.html', {'courses':courses, 'student':student, 'semesters':SEM_CHOICES})

def postCourses(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    semester = request.GET.get('semester')
    courses_data = selectedcourses.objects.all().filter(student_id = student).filter(semester=semester)
    context = { 'courses' : courses_data}
    return render(request, 'student/courseslist.html', context)
    
def postGrades(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    semester = request.GET.get('semester')
    grades_data =  studentgrades.objects.filter(application_id__student_id=student).filter(application_id__semester=semester).exclude(marks=-1)
    remaining = studentgrades.objects.filter(application_id__student_id=student).filter(application_id__semester=semester).filter(marks=-1)
    context = {'records':grades_data, 'remaining':remaining}
    return render(request, 'student/grades.html', context)

def postExams(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    semester = request.GET.get('semester')
    exams_data = studentgrades.objects.all().filter(application_id__student_id = student).filter(application_id__semester=semester)
    return render(request, 'student/exams.html', {'exams': exams_data})


def testexamAjax(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    exam_data = request.GET.get('exams')
    exams = json.loads(exam_data)
    print(exams)
    exams_list=[]
    i=0
    while(i<len(exams)):
        exams_list.append(get_object_or_404(Exams, pk=exams[str(i)]))
        i+=1
    
    for exam in exams_list:
        if (studentgrades.objects.filter(application_id__student_id=student)).filter(exam_id__subject_id=exam.subject_id).exists():
            exam.type="Chance"
        else:
            exam.type="Regular" 
    return render(request, 'student/selectedexams.html', {'exams':exams_list})

def confirmexamAjax(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    exam_data = request.GET.get('exam_data')
    exams = json.loads(exam_data)
    exams_list=[]
    i=0
    while(i<len(exams)):
        exams_list.append(get_object_or_404(Exams, pk=exams[str(i)]))
        i+=1

    for exam in exams_list:
        exam_check = (studentgrades.objects.filter(application_id__student_id=student)).filter(exam_id__subject_id=exam.subject_id).exists()
        obj = application_form(student=student, exam=exam, exam_type="CHA" if exam_check else "REG")
        obj.save()
    
    return JsonResponse({"a":"b"})

def addAjax(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    search_string = request.GET.get("search_string")
    course_list = []
    course_all = Subject.objects.all()
    for course in course_all:
        if search_string in course.subject_code:
                course_list.append(course)
            
    selected_courses = selectedcourses.objects.filter(student_id=student)
    a_list=[]
    for course in selected_courses:
        a_list.append(course.subject_id)

    final_list = list(set(course_list) - set(a_list))

    return render(request, 'student/courseaddlist.html', {'courses':final_list})

def confirmAjax(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    course_code = request.GET.get("course_id")
    student_object = student
    course_object = get_object_or_404(Subject, subject_code = course_code)

    to_add = selectedcourses (subject_id=course_object, student_id=student_object, year = date1.now().year, semester=student_object.semester)
    to_add.save() 
    # messages.success(request, 'Course ' + course_object.subject_name + ' added.')
    # return redirect('student:addcourse')
    return HttpResponseRedirect(reverse('student:addcourse'))

def login(request):
    return render(request, 'student/login.html')

def viewform(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    term = get_object_or_404(Term, pk=request.POST['term'])
    count = int(request.POST['count'])
    exams=[]
    i=0

    while(i<count):
        exams.append(get_object_or_404(Exams, pk=request.POST[str(i)]))
        i+=1
    
    print(exams)

    context={
        'term':term,
        'student':student,
        'exams': exams
    }
    return render(request, 'student/view_form.html', context)

def student_application(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])
    term = get_object_or_404(Term, pk=request.POST['term'])
    count = int(request.POST['count'])
    app_id = request.POST['application_id']
    exams=[]
    i=0

    app_obj = application_form(application_id=app_id, student=student, term=term, semester=student.semester)

    if (application_form.objects.filter(application_id=app_id).exists()):
        # messages.error(request, 'You have already applied.')
        url='{% url "student:checkscore" %}'
        # messages.error(request, 'Application failed. Go to <a href="{% url \'student:checkscore\' %}">link</a>', extra_tags='safe')
        # messages.error(request, f'Application failed. Go to <a href={url}>link</a>', extra_tags='safe')
        messages.success(request, 'Application failed. <a href="printapplicationform">Test link</a><br>Or access the page from sidebar.', extra_tags='safe')
        return HttpResponseRedirect(reverse('student:index'))
    else:
        app_obj.save()

        while(i<count):
            exams.append(get_object_or_404(Exams, pk=request.POST[str(i)]))
            i+=1
    
        for item in exams:
            app_obj.exam.add(item, through_defaults={'exam_type':True, 'passed':False})
        
        app_obj.save()
        
        messages.success(request, 'Application successful. Print form <a href="printapplicationform">here</a>', extra_tags='safe')
        return HttpResponseRedirect(reverse('student:index'))

def printresults(request):
    return render (request, 'student/print_results.html')

def printadmitcard(request):
    student = get_object_or_404(Student, student_id = request.session['user_id'])

    context={'student':student}
    return render (request, 'student/print_admitcard.html', context)

def printapplicationform(request):
    return render(request, 'student/print_applicationform.html')
