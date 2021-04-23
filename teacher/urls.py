from django.urls import path
from . import views

app_name = 'teacher'

urlpatterns=[
    path('home', views.index, name='index'),
    path('addscore', views.addscore, name='addscore'),
    path('addscore/code', views.subscore, name='subscore'),
    path('submitscore', views.submitscore, name='submitscore'),
    path('checkscore', views.checkscore, name='checkscore'),
    path('login', views.login, name = "login"),
    path('uploadcsv', views.uploadcsv, name = "uploadcsv"),
    path('logout', views.logout, name = "logout"),
    path('exportcsv/<str:exam_id>', views.exportcsv, name = "exportcsv"),
    path('studentlist', views.studentlist, name='studentlist'),
    path('ajax/studentlist', views.examsAjax, name='examsAjax'),
    path('ajax/loadExamsAjax', views.loadExamsAjax, name='loadExamsAjax'),
]