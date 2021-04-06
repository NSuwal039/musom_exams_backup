from django.urls import path
from . import views

app_name = 'student'

urlpatterns=[
    path('home', views.index, name='index'),
    path('checkscore', views.checkscore, name='checkscore'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('registerexam', views.registerexam, name='registerexam'),
    path('examapplication', views.examapplication, name='examapplication'),
    path('examdetails', views.examdetails, name='examdetails'),
    path('viewcourses', views.viewcourses, name='viewcourses'),
    path('printform', views.printform, name='printform'),
    path('student_application', views.student_application, name='student_application'),
    path('print_results', views.printresults, name='printresults'),
    path('print_admitcard', views.printadmitcard, name='printadmitcard'),
    path('ajax/examslist', views.examslist, name = "examslist"),
    path('ajax/testexamAjax', views.testexamAjax, name = "testexamAjax"),
    path('ajax/confirmexamAjax', views.confirmexamAjax, name = "confirmexamAjax"),
    path('ajax/courses', views.postCourses, name = "postCourses"),
    path('ajax/grades', views.postGrades, name = "postGrades"),
    path('ajax/exams', views.postExams, name = "postExams"),
    path('ajax/addcourse', views.addAjax, name = "addAjax"),
    path('ajax/confirmcourse', views.confirmAjax, name = "confirmAjax"),
    path('login', views.login, name = "login"),
]