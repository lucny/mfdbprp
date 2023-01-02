from django.urls import path
from movies import views
from graphene_django.views import GraphQLView
from movies.schema import schema
from django.views.decorators.csrf import csrf_exempt
from graphql_jwt.decorators import jwt_cookie

urlpatterns = [
    # cesta (route) pro zobrazení úvodní stránky
    path('', views.index, name='index'),
    # cesta pro zobrazení seznamu filmů
    path('films/', views.FilmListView.as_view(), name='films'),
    # cesta pro zobrazení podrobností o filmu definovaném atributem pk - <int:pk> (celočíselnou hodnotou primárního klíče)
    path('films/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),
    # cesta pro zobrazení seznamu filmů vybraného žánru podle hodnoty v atributu genre_name - <str:genre_name> (typu string)
    path('films/genres/<str:genre_name>/', views.FilmListView.as_view(), name='film-genre'),
    # cesta pro vytvoření nového záznamu o filmu
    path('films/create/', views.FilmCreate.as_view(), name='film_create'),
    # cesta pro aktualizaci záznamu o vybraném filmu (podle primárního klíče - pk)
    path('films/<int:pk>/update/', views.FilmUpdate.as_view(), name='film_update'),
    # cesta pro odstranění záznamu o vybraném filmu (podle primárního klíče - pk)
    path('films/<int:pk>/delete/', views.FilmDelete.as_view(), name='film_delete'),
    path('clear_cache/', views.clear_cache),
    # path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path("graphql/", jwt_cookie(GraphQLView.as_view(graphiql=True, schema=schema))),
]