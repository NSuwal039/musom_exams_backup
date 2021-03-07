from django.urls import path
from . import views

app_name = 'courses'

urlpatterns=[
    path('', views.index, name='index'),
    path('addcourse', views.addcourse, name='addcourse'),
    path('addexam', views.addexam, name='addexam'),
    path('examresults', views.examresults, name='examresults'),
    path('viewresults', views.viewresults, name='viewresults'),
    path('ajax/subjectAjax', views.subjectAjax, name = "subjectAjax"),
    path('ajax/termAjax', views.termAjax, name = "termAjax"),
    path('ajax/yearAjax', views.yearAjax, name = "yearAjax"),
]