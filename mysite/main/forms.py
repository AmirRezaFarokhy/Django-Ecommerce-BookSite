from .models import Books
from simple_search import search_form_factory

SearchForm = search_form_factory(Books.objects.all(),
                                 ['^title', 'description'])

