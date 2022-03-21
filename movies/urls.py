from django.urls import path, include
from movies import views

urlpatterns = [
    path('', views.index, name='index'),
    path('films/', views.FilmListView.as_view(), name='films'),
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),
]