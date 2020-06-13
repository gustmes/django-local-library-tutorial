from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my_borrowed'),
    path('borrowed/', views.BorrowedBooksListView.as_view(), name='borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew_book_librarian'),
    path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('authors/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('authors/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('books/create/', views.BookCreate.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('books/borrow/<uuid:id>/', views.book_borrow, name='book_borrow'),
]
