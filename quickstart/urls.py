from django.urls import path
from .views import RegisterView, LoginView, BookList, BookCreate, BookIssueCreate, BookReturnUpdate, user_book_list

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/add/', BookCreate.as_view(), name='book-create'),
    path('books/issue/', BookIssueCreate.as_view(), name='book-issue'),
    path('books/return/<int:pk>/', BookReturnUpdate.as_view(), name='book-return'),
    path('books/user/', user_book_list, name='user-book-list'),
]