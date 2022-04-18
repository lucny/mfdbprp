from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import FilmModelForm
from .models import Film, Genre, Attachment


def index(request):
    """Metoda připravuje pohled pro domovskou stránku - šablona index.html"""

    # Uložení celkového počtu filmů v databázi do proměnné num_films
    num_films = Film.objects.all().count()
    # Do proměnné films se uloží 3 filmy uspořádané podle hodnocení (sestupně)
    films = Film.objects.order_by('-rate')[:3]

    """ Do proměnné context, která je typu slovník (dictionary) uložíme hodnoty obou proměnných """
    context = {
        'num_films': num_films,
        'films': films,
        'genres': Genre.objects.order_by('name').all(),
        'top_tens': Film.objects.order_by('-rate').all()[:10]
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

    def get_queryset(self):
        if 'genre_name' in self.kwargs:
            return Film.objects.filter(genres__name=self.kwargs['genre_name']).all() # Get 5 books containing the title war
        else:
            return Film.objects.all()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['num_films'] = len(self.get_queryset())
        if 'genre_name' in self.kwargs:
            context['view_title'] = f"Žánr: {self.kwargs['genre_name']}"
            context['view_head'] = f"Žánr filmu: {self.kwargs['genre_name']}"
        else:
            context['view_title'] = 'Filmy'
            context['view_head'] = 'Přehled filmů'
        return context


""" Třída dědí z generické třídy DetailView, která umí vypsat z databáze jeden objekt určeného modelu """
class FilmDetailView(DetailView):
    # Nastavení požadovaného modelu
    model = Film
    # Pojmenování objektu, v němž budou šabloně předána data z modelu (tj. databázové tabulky)
    context_object_name = 'film_detail'
    # Umístění a název šablony
    template_name = 'film/detail.html'


class GenreListView(ListView):
    model = Genre
    template_name = 'blocks/genre_list.html'
    context_object_name = 'genres'
    queryset = Genre.objects.order_by('name').all()


class FilmCreate(CreateView):
    model = Film
    template_name = 'movies/film_form_crispy.html'
    fields = ['title', 'plot', 'release_date', 'runtime', 'poster', 'rate', 'genres']
    initial = {'rate': '5'}

    def get_success_url(self):
        return reverse_lazy('film_detail', kwargs={'pk': self.object.pk})


class FilmUpdate(UpdateView):
    model = Film
    template_name = 'movies/film_bootstrap_form.html'
    form_class = FilmModelForm
    #fields = '__all__' # Not recommended (potential security issue if more fields added)

    def get_success_url(self):
        return reverse_lazy('film_detail', kwargs={'pk': self.object.pk})


class FilmDelete(DeleteView):
    model = Film
    success_url = reverse_lazy('films')