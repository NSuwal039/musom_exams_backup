from json.encoder import JSONEncoder
from django import forms
from django.db.models import Q
from django.http.response import HttpResponse, JsonResponse
from student.models import Student
from django.contrib import messages 
from django.shortcuts import redirect, render, get_object_or_404
from teacher.models import Teacher
from .models import Subject, Term, application_form, selectedcourses, studentgrades
from .models import Exams
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import CoursesForm, ExamsForm

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
            messages.success(request, 'Course info added.')
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
            messages.success(request, 'Exam info added.')
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
        if student_id in student.pk:
            student_list.append(student)
    
    return render(request, 'courses/studentlist.html',{'students':student_list})

def studentsmarksentry(request, id):
    student = get_object_or_404(Student, pk=id)
    exams = studentgrades.objects.filter(student_id = student)
    return render(request, 'courses/studentmarksentry.html', {'student': student, 'exams':exams})

def submitscores(request):
    student = get_object_or_404(Student, pk=request.POST['student_id'])
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
            messages.success(request, 'Marks entry successful.')
            print(messages)
        else:
            if request.POST[exam.exam_id.exam_title]:
                marks=marks
            else:
                marks=0        
            exam_marks = studentgrades( student_id=student_object, exam_id=exam_object, marks=marks)
            exam_marks.save()
            messages.success(request, 'Marks entry successful.')
            print (messages)

    return HttpResponseRedirect(reverse('courses:index'))

def confirmexamapplication(request):
    return render(request, 'courses/confirmexamapplication.html')

def confirmAjax(request):
    form_id = request.GET.get('form_id')
    form = application_form.objects.filter(Q(application_id__icontains=form_id),Q(status=False))
    print(form)
    return render(request, 'courses/examapplication.html', {'form':form})

def confirmapplication(request):
    app_id = request.GET.get('application_radio')
    application = get_object_or_404(application_form, pk=app_id)
    application.status=True
    application.save()
    
    messages.success(request, "Registration confirmed.")
    return HttpResponseRedirect(reverse('courses:index'))

def bulkprintadmitcard(request):
    terms = Term.objects.all()

    context = {'terms':terms}
    return render(request, 'courses/bulkprintadmitcard.html',context)

def returnexamdropdown(request):
    term = get_object_or_404(Term, pk=request.GET.get('term_id'))
    exams = Exams.objects.filter(term=term)

    context = {"exams":exams}
    return render(request, "courses/showexamdropdown.html", context)

def return_exams_admit(request):
    search_string= request.GET.get('exam_id')
    exams = Exams.objects.filter(exam_id__icontains=search_string)
    
    return render(request, "courses/showexamlist_admit.html", {'exams':exams})

def returnstudentlist_admit(request):
    applications = application_form.objects.filter(exam=get_object_or_404(Exams, pk=request.GET.get('exam_id'))).filter(status=True)
    
    context = {'applications':applications,
                'exam':get_object_or_404(Exams, pk=request.GET.get('exam_id'))}
    return render(request, 'courses/showadmitcardlist.html', context)

def printadmitcards(request):
    count = int(request.POST.get("count"))
    i = 1
    applications = []
    while (i<=count):
        applications.append(get_object_or_404(application_form, pk=request.POST.get(str(i))))
        i+=1
    
    gradeinfo = studentgrades.objects.none()

    for item in applications:
        gradeinfo = gradeinfo|(studentgrades.objects.filter(application_id=item))

    print(str(gradeinfo) + "\n___________________________________________")

    context = {'applications':applications,
                'gradeinfo':gradeinfo}
    return render(request, "courses/showbulkprintadmit.html", context)

#----------------------------------------------------------------------------------------------------------------------

#bulk print results#

def bulkprintresults(request):
    terms = Term.objects.all()

    context = {'terms':terms}
    return render(request, 'courses/bulkprintresults.html',context)

def return_exams_results(request):
    search_string= request.GET.get('exam_id')
    exams = Exams.objects.filter(exam_id__icontains=search_string)
    
    return render(request, "courses/showexamlist_results.html", {'exams':exams})

def returnstudentlist_results(request):
    applications = application_form.objects.filter(exam=get_object_or_404(Exams, pk=request.GET.get('exam_id'))).filter(status=True)
    
    context = {'applications':applications,
                'exam':get_object_or_404(Exams, pk=request.GET.get('exam_id'))}
    return render(request, 'courses/showresultslist.html', context)

def printresults(request):
    count = int(request.POST.get("count"))
    i = 1
    applications = []
    gradeinfo = studentgrades.objects.none()
    students = []
    no_results = []

    while (i<=count):
        applications.append(get_object_or_404(application_form, pk=request.POST.get(str(i))))
        i+=1
    
    for item in applications:
        students.append(item.student)
    
    for item in applications:
        gradeinfo = gradeinfo|studentgrades.objects.filter(Q(application_id=item)&Q(passed=True)).order_by('-marks')[0:4]

    for student in students:
        i=0
        for item in gradeinfo:
            if item.application_id.student == student:
                i+=1
        
        if i==0:
            no_results.append(student)
        

    context = {'applications':applications,
                'gradeinfo':gradeinfo,
                'noresults':no_results}
    return render(request, "courses/showbulkprintresults.html", context)

def viewstudentlist(request):
    year=selectedcourses._meta.get_field('year').choices
    year_choices = [ i[1] for i in year]

    if request.method=='GET':
        
        context={'year':year_choices}
        return render(request, 'courses/viewstudentlist.html', context)
    else:
        selected_year = request.POST['year']
        subject_code = request.POST['subject']
        subject = Subject.objects.filter(pk=subject_code)
        context={'year':year_choices}
        records = selectedcourses.objects.none()

        if (subject):
            records = selectedcourses.objects.filter(Q(year=selected_year)&Q(subject_id=subject[0]))

        if (records):
            context['records']=records
            return render(request, 'courses/viewstudentlist.html', context)
        else:
            messages.error(request, "Record not found.")
            return render (request, 'courses/viewstudentlist.html', context)
        
        

