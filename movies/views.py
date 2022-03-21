from django.shortcuts import render
from movies.models import Film


def index(request):
    """View function for home page of site."""
    num_films = Film.objects.all().count()
    films = Film.objects.order_by('-rate')[:3]

    context = {
        'num_films': num_films,
        'films': films
    }

    return render(request, 'index.html', context=context)

