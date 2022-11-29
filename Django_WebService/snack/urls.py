from django.urls import path
from . import views

app_name = 'snack'

urlpatterns = [
    path('', views.index, name='index'),
]