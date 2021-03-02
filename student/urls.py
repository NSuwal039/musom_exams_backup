from django.urls import path
from . import views

app_name = 'student'

urlpatterns=[
    # path('login', views.login, name='login'),
    path('home', views.index, name='index'),
    path('checkscore', views.checkscore, name='checkscore'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('registerexam', views.registerexam, name='registerexam'),
    path('examdetails', views.examdetails, name='examdetails'),
    path('viewcourses', views.viewcourses, name='viewcourses')
]