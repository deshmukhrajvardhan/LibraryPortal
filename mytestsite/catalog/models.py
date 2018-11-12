from django.db import models
from django.urls import reverse
import uuid  # Required for unique book instances

# Create your models here.


class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200,
                            help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-details', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return '{}, {}'.format(self.last_name, self.first_name)


class Language(models.Model):
    LANG_LIST = []
    index = 1
    with open('/home/rajvardhan/PycharmProjects/LibraryPortal/mytestsite/catalog/languages.txt', 'r') as read_lang:
        lang = read_lang.readline()
        while lang != '':
            LANG_LIST.append((index, lang))
            index += 1
            lang = read_lang.readline()
            # print(LANG_LIST)

    name = models.IntegerField(
        # max_length=100,
        choices=LANG_LIST,
        blank=True,
        default=38,  # English
        help_text='Choose Language',
    )

    def __str__(self):
        # Lists all languages
        return '{}'.format(self.LANG_LIST[self.name-1][1])


class Book(models.Model):
    # Fields
    title = models.CharField(max_length=200, help_text='Enter title')
    # author = Author()
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(help_text='Enter summary')
    isbn = models.CharField('ISBN', max_length=20, help_text='Enter field documentation')
    pubdate = models.DateField(help_text='Enter date of publication')
    genre = models.ManyToManyField(Genre, help_text='Select genre for this book')
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    # Meta
    class Meta:
        ordering = ['title', '-pubdate']

    # Methods
    def __str__(self):
        return self.title

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-details', args=[str(self.id)])


class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object."""
        return '{}({})'.format(self.id, self.book.title)
