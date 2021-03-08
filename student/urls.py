from django.urls import path
from . import views

app_name = 'student'

urlpatterns=[
    path('home', views.index, name='index'),
    path('checkscore', views.checkscore, name='checkscore'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('registerexam', views.registerexam, name='registerexam'),
    path('examdetails', views.examdetails, name='examdetails'),
    path('viewcourses', views.viewcourses, name='viewcourses'),
    path('ajax/courses', views.postCourses, name = "postCourses"),
    path('ajax/grades', views.postGrades, name = "postGrades"),
    path('ajax/exams', views.postExams, name = "postExams"),
    path('ajax/addcourse', views.addAjax, name = "addAjax"),
    path('ajax/confirmcourse', views.confirmAjax, name = "confirmAjax"),
    path('login', views.login, name = "login"),
]