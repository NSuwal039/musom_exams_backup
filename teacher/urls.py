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
    path('studentlist', views.studentlist, name='studentlist'),
    path('ajax/studentlist', views.examsAjax, name='examsAjax'),
    path('ajax/loadExamsAjax', views.loadExamsAjax, name='loadExamsAjax'),
]