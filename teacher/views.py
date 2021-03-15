from django.contrib import messages
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from courses.models import studentgrades, Exams, Subject, selectedcourses
from .models import Teacher 
from student.models import Student
from django.urls import reverse
from .forms import gradesform


def index(request):
    if request.method == 'POST':
        request.session['teacherID'] = request.POST['teacherID']
    teacher = get_object_or_404(Teacher, teacher_id = request.session['teacherID'])
    return render (request, 'teacher/index.html', {'teacher':teacher})

def addscore(request):
    teacher = get_object_or_404(Teacher, teacher_id = request.session['teacherID'])
    if request.method=='GET':
        subject = Subject.objects.all().filter(teacher_id=teacher)
        exams = Exams.objects.all().filter(subject_id__in=subject)
        return render(request, 'teacher/addscore.html', {'teacher': teacher, 'subject':subject,'exams':exams})

def subscore(request):
    teacher = get_object_or_404(Teacher, teacher_id = request.session['teacherID'])
    exam_code = request.GET['exam']
    selected_exam = get_object_or_404(Exams, exam_id=exam_code)
    selected_subject=selected_exam.subject_id
    existing_records = studentgrades.objects.all().filter(exam_id=selected_exam)
    student_data = selectedcourses.objects.all().filter(subject_id = selected_subject)
    
    # form = gradesform()
    context = {'teacher': teacher,  'students':student_data, 'exam':selected_exam}
    return render (request, 'teacher/dump.html', context )

def submitscore(request):
    teacher = get_object_or_404(Teacher, teacher_id = request.session['teacherID'])
    exam = get_object_or_404(Exams, exam_id=request.POST['exam_id'])
    selected_subject = exam.subject_id
    students = studentgrades.objects.filter(exam_id__subject_id=selected_subject)
    # student_list=[]
    
    new=0
    for stu in students:
        student_object = stu.student_id
        exam_object = exam
        marks = request.POST[stu.student_id.student_id]
        f_marks=int(marks)
        test = studentgrades.objects.all().filter(student_id=student_object, exam_id= exam_object)
        if test.exists():
            editobject = studentgrades.objects.get(student_id=student_object, exam_id= exam_object)
            if request.POST[stu.student_id.student_id]:
                editobject.marks=f_marks
            else:
                pass
            messages.success(request, 'Marks entry successful.')
            editobject.save()
        else:
            if request.POST[stu.student_id.student_id]:
                marks=f_marks
            else:
                marks=0        
            exam_marks = studentgrades( student_id=student_object, exam_id=exam_object, marks=marks)
            messages.success(request, 'Marks entry successful.')
            exam_marks.save()
            new+=1

    return HttpResponseRedirect(reverse('teacher:index'))

def studentlist(request):
    teacher = get_object_or_404(Teacher, teacher_id = request.session['teacherID'])
    return render (request, 'teacher/studentlist.html', {'teacher':teacher})

    
def checkscore(request):
    teacher = get_object_or_404(Teacher, teacher_id = request.session['teacherID'])
    subjects = Subject.objects.all().filter(teacher_id=teacher)
    exams = Exams.objects.all().filter(subject_id__in=subjects)

    if request.method=='GET':
        return render(request, 'teacher/checkscore.html', {'exams':exams, 'teacher':teacher})
    else:
        code=1
        selected_exam = get_object_or_404(Exams, exam_id=request.POST['exam_id'])
        studentrecords = studentgrades.objects.all().filter(exam_id=selected_exam).exclude(marks=-1)
        selected_object = request.POST['exam_id']
        context = {'teacher':teacher,'students':studentrecords, 'exams':exams, 'selected_exam':selected_exam, 'code':code}
        return render(request, 'teacher/checkscore.html', context)

def examsAjax(request):
    # teacher = get_object_or_404(Teacher, teacher_id = request.session['teacherID'])
    exam_id = request.GET.get('exam_id')
    selected_exam = get_object_or_404(Exams, exam_id=exam_id)
    student_data = studentgrades.objects.all().filter(exam_id=selected_exam)

    return render (request, 'teacher/submit_score.html', {'students':student_data, 'exam':selected_exam})

def login(request):
    return render(request, 'teacher/login.html')
        