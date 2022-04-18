from django.urls import path, include
from movies import views

urlpatterns = [
    path('', views.index, name='index'),
    path('films/', views.FilmListView.as_view(), name='films'),
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),
    path('films/genres/<str:genre_name>/', views.FilmListView.as_view(), name='film-genre'),
    path('films/create/', views.FilmCreate.as_view(), name='film_create'),
    path('films/<int:pk>/update/', views.FilmUpdate.as_view(), name='film_update'),
    path('films/<int:pk>/delete/', views.FilmDelete.as_view(), name='film_delete'),
]