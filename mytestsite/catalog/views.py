from django.shortcuts import render
from django.views import generic
# Create your views here.
from catalog.models import Book, Author, BookInstance, Genre


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'library_book_list'  # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='were')[:5]  # Get 5 books containing the title were
    template_name = 'books/library_book_list.html'  # Specify your own template name/location

    def get_queryset(self):
        return Book.objects.filter(title__icontains='were')[:5]  # Get 5 books containing the title were

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        # Context is a dict
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'author_list'  # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains='were')[:5]  # Get 5 books containing the title were
    template_name = 'authors/author_list.html'  # Specify your own template name/location

    def get_queryset(self):
        return Author.objects.all()[:5]  # Get 5 books containing the title were

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        # Context is a dict
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_genre_with_a = Genre.objects.filter(name__icontains='a').count()

    num_books_with_a = Book.objects.filter(title__icontains='a').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre_with_a': num_genre_with_a,
        'num_books_with_a': num_books_with_a,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookDetailView(generic.DetailView):
    model = Book
    paginate_by = 10
    template_name = 'book_details.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10
    template_name = 'author_details.html'