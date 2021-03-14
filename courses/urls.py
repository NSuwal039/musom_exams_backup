from django.urls import path
from . import views

app_name = 'courses'

urlpatterns=[
    path('', views.index, name='index'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('addexam', views.addexam, name='addexam'),
    path('examresults', views.examresults, name='examresults'),
    path('viewresults', views.viewresults, name='viewresults'),
    path('examtoppers', views.examtoppers, name='examtoppers'),
    path('addstudentmarks', views.addstudentmarks, name='addstudentmarks'),
    path('submitscores', views.submitscores, name='submitscores'),
    path('confirmexamapplication', views.confirmexamapplication, name='confirmexamapplication'),
    path('studentmarksentry/<str:id>', views.studentsmarksentry, name='studentmarksentry'),
    path('ajax/studentlist', views.studentsAjax, name='studentlist'),
]