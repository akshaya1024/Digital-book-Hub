from django.urls import path

from . import views
urlpatterns = [
    path('books/', views.books, name="books"),
    path('view_books/', views.view_books, name="view_books"),
    path('add_books/', views.add_book, name="add_book"),
    path('update_books/', views.update_books, name='update_books'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_books/', views.delete_books, name='delete_books'),
    path('confirm_delete/<int:book_id>/', views.confirm_delete, name='confirm_delete'),
    path('students/', views.students, name="students"),
    path('view_student/', views.view_student, name="view_student"),
    path('add_student/', views.add_student, name="add_student"),
    path('update_student/', views.update_student, name='update_student'),
    path('edit_student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete_student/', views.delete_student, name='delete_student'),
    path('confirm_student_delete/<int:student_id>/', views.confirm_student_delete, name='confirm_student_delete'),
    path("issue-book/", views.issue_book, name="issue_book"),
    path("search-student/", views.search_student, name="search_student"),
    path("search-book/", views.search_book, name="search_book"),
    path("issued-books/", views.issued_books, name="issued_books"),
    path("return-book/<int:issue_id>/", views.return_book, name="return_book"),

]






