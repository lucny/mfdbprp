from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import FilmModelForm
from .models import Film, Genre, Attachment


def index(request):
    """Metoda připravuje pohled pro domovskou stránku - šablona index.html"""
    """ Do proměnné context, která je typu slovník (dictionary), přiřadíme jednotlivým klíčům informace získané z databáze
     pomocí ORM systému Djanga - využíváme jednotlivých datových modelů a pracujeme s nimi jako se sadami objektů """
    context = {
        # Výběr filmů podle data uvedení uspořádaný sestupně - 3 nejnovější filmy
        'films': Film.objects.order_by('-release_date')[:3],
        # Výběr deseti nejlepších filmů (uspořádány sestupně podle hodnocení)
        'top_ten': Film.objects.order_by('-rate').all()[:10],
        # Výběr všech žánrů uspořádaných abecedně podle názvu
        'genres': Genre.objects.order_by('name').all(),
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

    # Metoda vrací sadu záznamů filtrovaných podle nastavení klíčového argumentu 'genre_name'
    def get_queryset(self):
        # Jestliže je v klíčových atributech předaných objektu (self.kwargs) zastoupen atribut 'genre_name' ...
        if 'genre_name' in self.kwargs:
            # ... z databáze jsou vybrány všechny objekty (filmy), patřící k žánru, na který klíčový atribut odkazuje
            # genres__name=self.kwargs['genre_name']
            return Film.objects.filter(genres__name=self.kwargs['genre_name']).all()
        else:
            # ... v opačném případě jsou vybrány všechny objekty (filmy)
            return Film.objects.all()

    # Metoda upravuje data předávaná šabloně prostřednictví proměnné context (typu dictionary)
    def get_context_data(self, **kwargs):
        # Nejprve je zavolána původní implementace metody, jak je řešena v třídě předka, který zastupuje dočasný objekt super()
        # (temporary object of the superclass)
        context = super().get_context_data(**kwargs)
        # Zjištění aktuálního počtu záznamů v dané datové sadě - len(self.get_queryset())
        context['num_films'] = len(self.get_queryset())
        # Jestliže je v klíčových atributech předaných objektu (self.kwargs) zastoupen atribut 'genre_name' ...
        if 'genre_name' in self.kwargs:
            # ... šabloně budou prostřednictvím kontextu předány proměnné 'view_title' a 'view_head', které budou obsahovat informace
            # o aktuálně vybraném žánru
            context['view_title'] = f"Žánr: {self.kwargs['genre_name']}"
            context['view_head'] = f"Žánr filmu: {self.kwargs['genre_name']}"
        else:
            # ... v opačném případě budou předány stejné proměnné s obecnějším popisem
            # o aktuálně vybraném žánru
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