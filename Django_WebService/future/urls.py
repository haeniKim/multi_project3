from django.urls import path
from . import views

app_name = 'future'

urlpatterns = [
    path('', views.index, name='index'),
]