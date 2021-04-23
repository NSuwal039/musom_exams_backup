from django.contrib import messages
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from courses.models import Term, application_form, studentgrades, Exams, Subject, selectedcourses
from .models import Teacher 
from student.models import Student
from django.urls import reverse
import csv, io
from django.db.models import Q


def index(request):
    if request.method == 'POST':
        request.session['teacherID'] = request.POST['teacherID']
    teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    return render (request, 'teacher/index.html', {'teacher':teacher})

def addscore(request):
    teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    terms = Term.objects.all()
    if request.method=='GET':
        subject = Subject.objects.all().filter(teacher_id=teacher)
        exams = Exams.objects.all().filter(subject_id__in=subject)
        return render(request, 'teacher/addscore.html', {'teacher': teacher, 'subject':subject,'exams':exams, 'terms':terms})

def subscore(request):
    teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    exam_code = request.GET['exam']
    selected_exam = get_object_or_404(Exams, exam_id=exam_code)
    selected_subject=selected_exam.subject_id
    # existing_records = studentgrades.objects.all().filter(exam_id=selected_exam)
    student_data = selectedcourses.objects.all().filter(subject_id = selected_subject)
    
    # form = gradesform()
    context = {'teacher': teacher,  'students':student_data, 'exam':selected_exam}
    return render (request, 'teacher/dump.html', context )

def submitscore(request):
    teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    exam = get_object_or_404(Exams, exam_id=request.GET['exam_id'])
    selected_subject = exam.subject_id
    print("subject: " + selected_subject.__str__())
    students = studentgrades.objects.filter(exam_id__subject_id=selected_subject)
    # print(list(request.GET.items()))
    
    failed_attempts=[]
    entries=0;
    if (students):
        for student in students:
            try:
                marks=int(request.GET[student.application_id.student.student_id])
                student.marks = marks
                student.save()
                entries+=1
            except:
                failed_attempts.append(student.application_id.student)
    else:
        print("Error")
    
    if (len(failed_attempts)==0):
        messages.success(request, "Marks entry for " + str(entries) + " students successful")
        return HttpResponseRedirect(reverse('teacher:index'))
    else:
        messages.error(request, "Marks entry for " + str(len(failed_attempts)) + " students unsuccessful")
        return HttpResponseRedirect(reverse('teacher:index'))

def studentlist(request):
    teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    return render (request, 'teacher/studentlist.html', {'teacher':teacher})

    
def checkscore(request):
    teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    subjects = Subject.objects.all().filter(teacher_id=teacher)
    exams = Exams.objects.all().filter(subject_id__in=subjects)

    if request.method=='GET':
        return render(request, 'teacher/checkscore.html', {'exams':exams, 'teacher':teacher})
    else:
        code=1
        selected_exam = get_object_or_404(Exams, exam_id=request.POST['exam_id'])
        studentrecords = studentgrades.objects.filter(exam_id=selected_exam).exclude(marks=-1)
        studentrecords_remaining = studentgrades.objects.filter(exam_id=selected_exam).filter(marks=-1)
        context = {'teacher':teacher,'students':studentrecords, 'exams':exams, 'selected_exam':selected_exam, 'code':code, 'remaining':studentrecords_remaining}
        return render(request, 'teacher/checkscore.html', context)

def examsAjax(request):
    # teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    exam_id = request.GET.get('exam_id')
    selected_exam = get_object_or_404(Exams, exam_id=exam_id)
    student_data = studentgrades.objects.all().filter(exam_id=selected_exam)

    return render (request, 'teacher/submit_score.html', {'students':student_data, 'exam':selected_exam})

def login(request):
    return render(request, 'teacher/login.html')

def loadExamsAjax(request):
    teacher = teacher = get_object_or_404(Teacher, pk = request.session['teacherID'])
    term = get_object_or_404(Term, pk=request.GET.get('term_id'))
    subject = Subject.objects.all().filter(teacher_id=teacher)
    exams = Exams.objects.all().filter(Q(subject_id__in=subject) & Q(term=term))
    return render(request, 'teacher/examslist.html', {'exams':exams})

def exportcsv(request, exam_id):
    selected_exam = get_object_or_404(Exams, exam_id=exam_id)
    student_data = studentgrades.objects.all().filter(exam_id=selected_exam)
    student_data = studentgrades.objects.all().filter(exam_id=selected_exam)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "results.csv"'

    writer = csv.writer(response, delimiter=",")
    writer.writerow(['exam_id','application_id', 'name','marks','exam_type'])

    for obj in student_data:
        writer.writerow([obj.exam_id.exam_id, obj.application_id.application_id,obj.application_id.student.student_name, "", obj.exam_type])
    
    return response

def uploadcsv(request):
    csv_file = request.FILES['file']

    if not csv_file.name.endswith('.csv'):
        messages.error(request, "Invalid file")
    
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)

    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            gradeobj = get_object_or_404(studentgrades, exam_id=column[0], application_id=column[1])
            gradeobj.marks=int(column[3])
            gradeobj.save()
    
    messages.success(request,"Marks upload successful")
    return HttpResponseRedirect(reverse('teacher:index'))

def logout(request):
    del request.session['user_id']
    return render (request, "teacher/login.html")


        