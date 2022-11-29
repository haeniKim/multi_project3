from django.urls import path
from . import views

app_name = 'AboutUs'

urlpatterns = [
    path('', views.index, name='index'),
]