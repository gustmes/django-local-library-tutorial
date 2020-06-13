from django.db import models
from django.contrib.auth.models import User
from datetime import time, date

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200, help_text="Enter the book's natural language")

    def __str__(self):
        return self.name

from django.urls import reverse

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    #ManyToMany Key used because book can have more than one author, and an author can have more than one Book
    # Author as a string rather than object because it hasn't been declared yet
    authors = models.ManyToManyField('Author')

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book.')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    # Used for original Language
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])

    def display_authors(self):
        if self.authors.all().count() == 1:
            return self.authors.first()
        return '; '.join(author.get_short_name() for author in self.authors.all())
    display_authors.short_description = 'Authors'

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

import uuid

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    # Language of this specific BookInstance
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering= ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    def get_book_title(self):
        return self.book.title
    get_book_title.short_description = 'Book'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def save(self, *args, **kwargs):
        if self.status == 'a':
            self.due_back = None
            self.borrower = None
        super(BookInstance, self).save(*args, **kwargs)

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author_detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_short_name(self):
        return f'{self.last_name}, {self.first_name[0]}'
