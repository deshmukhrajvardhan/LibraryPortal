# Use include() to add paths from the catalog application
from django.urls import include
from django.urls import path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-details'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-details'),
    # path('url/', views.my_reused_view, {'my_template_name': 'some_path'}, name='aurl'),
    # path('anotherurl/', views.my_reused_view, {'my_template_name': 'another_path'}, name='anotherurl'),
    ]
