from django.urls import path, include
from movies import views

urlpatterns = [
    path('', views.index, name='index'),
]