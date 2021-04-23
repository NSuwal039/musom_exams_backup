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

    #bulk print admit cards
    path('bulkprintadmitcard', views.bulkprintadmitcard, name='bulkprintadmitcard'),
    path('printadmitcards', views.printadmitcards, name='printadmitcards'),
    path('ajax/returnexamdropdown', views.returnexamdropdown, name='returnexamdropdown'),
    path('ajax/return_exams_admit', views.return_exams_admit, name='return_exams_admit'),
    path('ajax/returnstudentlist_admit', views.returnstudentlist_admit, name='returnstudentlist_admit'),

    #bulk print results
    path('bulkprintresults', views.bulkprintresults, name='bulkprintresults'),
    path('ajax/return_exams_results', views.return_exams_results, name='return_exams_results'),
    path('ajax/returnstudentlist_results', views.returnstudentlist_results, name='returnstudentlist_results'),
    path('printresults', views.printresults, name='printresults'),

    path('confirmexamapplication', views.confirmexamapplication, name='confirmexamapplication'),
    path('studentmarksentry/<str:id>', views.studentsmarksentry, name='studentmarksentry'),
    path('confirmapplication', views.confirmapplication, name='confirmapplication'),
    path('ajax/studentlist', views.studentsAjax, name='studentlist'),
    path('ajax/confirmAjax', views.confirmAjax, name='confirmAjax'),
    
]