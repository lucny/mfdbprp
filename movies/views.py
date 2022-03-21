from django.shortcuts import render
from django.views.generic import ListView, DetailView

from movies.models import Film, Genre, Attachment


def index(request):
    """Metoda připravuje pohled pro domovskou stránku - šablona index.html"""

    # Uložení celkového počtu filmů v databázi do proměnné num_films
    num_films = Film.objects.all().count()
    # Do proměnné films se uloží 3 filmy uspořádané podle hodnocení (sestupně)
    films = Film.objects.order_by('-rate')[:3]

    """ Do proměnné context, která je typu slovník (dictionary) uložíme hodnoty obou proměnných """
    context = {
        'num_films': num_films,
        'films': films
    }

    """ Pomocí metody render vyrendrujeme šablonu index.html a předáme ji hodnoty v proměnné context k zobrazení """
    return render(request, 'index.html', context=context)


""" Třída dědí z generické třídy ListView, která umí vypsat z databáze všechny objekty určeného modelu """
class FilmListView(ListView):
    # Nastavení požadovaného modelu
    model = Film
    # Pojmenování objektu, v němž budou šabloně předána data z modelu (tj. databázové tabulky)
    context_object_name = 'films_list'
    # Umístění a název šablony
    template_name = 'film/list.html'


""" Třída dědí z generické třídy DetailView, která umí vypsat z databáze jeden objekt určeného modelu """
class FilmDetailView(DetailView):
    # Nastavení požadovaného modelu
    model = Film
    # Pojmenování objektu, v němž budou šabloně předána data z modelu (tj. databázové tabulky)
    context_object_name = 'film_detail'
    # Umístění a název šablony
    template_name = 'film/detail.html'