from django.shortcuts import render

# Create your views here.

def mainpage(request):
    return render(request, 'library_information/index.html')

def books(request):
    return render(request, 'library_information/books.html')

from .models import Books


def view_books(request):
    books = Books.objects.all()

    return render(
        request,
        'library_information/views-book.html',
        {'books': books}
    )
from django.shortcuts import render, redirect
from .models import Books

def add_book(request):
    if request.method == 'POST':
        book_name = request.POST.get('Book_name')
        author_name = request.POST.get('Author_name')
        quantity = request.POST.get('Quantity')

        Books.objects.create(
            Book_name=book_name,
            Author_name=author_name,
            Quantity=quantity
        )

        return redirect('view_books')

    return render(request, 'library_information/add_book.html')

from django.shortcuts import render, redirect, get_object_or_404
from .models import Books


def update_books(request):
    books = Books.objects.all()
    return render(
        request,
        'library_information/update_books.html',
        {'books': books}
    )


def edit_book(request, book_id):
    book = get_object_or_404(Books, Book_id=book_id)

    if request.method == 'POST':
        book.Book_name = request.POST.get('Book_name')
        book.Author_name = request.POST.get('Author_name')
        book.Quantity = request.POST.get('Quantity')
        book.save()

        return redirect('view_books')

    return render(
        request,
        'library_information/edit_book.html',
        {'book': book}
    )

from django.shortcuts import render, redirect, get_object_or_404
from .models import Books


def delete_books(request):
    books = Books.objects.all()
    return render(
        request,
        'library_information/delete_books.html',
        {'books': books}
    )


def confirm_delete(request, book_id):
    book = get_object_or_404(Books, Book_id=book_id)

    if request.method == 'POST':
        book.delete()
        return redirect('delete_books')

    return render(
        request,
        'library_information/confirm_delete.html',
        {'book': book}
    )

# Student inofmration

def students(request):
    return render(request, 'library_information/student.html')


from .models import Student


def view_student(request):
    student = Student.objects.all()

    return render(
        request,
        'library_information/view-student.html',
        {'student': student}
    )

from django.shortcuts import render, redirect
from .models import Student

def add_student(request):
    if request.method == 'POST':
        student_name = request.POST.get('Student_name')
        email = request.POST.get('Email')
        phoneno = request.POST.get('PhoneNo')
        department = request.POST.get('Department')

        Student.objects.create(
            Student_name=student_name,
            Email=email,
            PhoneNo = phoneno,
            Department = department
        )

        return redirect('view_student')

    return render(request, 'library_information/add_students.html')


def update_student(request):
    students = Student.objects.all()
    return render( request, 'library_information/update_student.html',
        {'students': students}
    )


def edit_student(request, student_id):
    student = get_object_or_404(Student, Student_id=student_id)

    if request.method == 'POST':
        student.Student_name = request.POST.get('Student_name')
        student.Email = request.POST.get('Email')
        student.PhoneNo = request.POST.get('PhoneNo')
        student.Department = request.POST.get('Department')
        student.save()

        return redirect('view_student')

    return render(request, 'library_information/edit_student.html',
        {'student': student}
    )



def delete_student(request):
    students = Student.objects.all()
    return render( request, 'library_information/delete_student.html',
        {'students': students}
    )


def confirm_student_delete(request, student_id):
    student = get_object_or_404(Student, Student_id=student_id)

    if request.method == 'POST':
        student.delete()
        return redirect('delete_student')

    return render(
        request,
        'library_information/confirm_student_delete.html',
        {'student': student}
    )

# Book Issue 

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from .models import Books, Student, BookIssue


# 1. Search Student
def search_student(request):
    student = None
    error = None
    student_id = ""

    if request.method == "POST":
        student_id = request.POST.get("student_id", "").strip()

        if student_id.isdigit():
            try:
                student = Student.objects.get(Student_id=int(student_id))
            except Student.DoesNotExist:
                error = "Student ID not found."
        else:
            error = "Please enter a valid Student ID."

    return render(request, "library_information/issue_book.html", {
        "student": student,
        "error": error,
        "student_id": student_id,
        "search_type": "student",
    })


# 2. Search Book
def search_book(request):
    book = None
    error = None
    book_id = ""

    if request.method == "POST":
        book_id = request.POST.get("book_id", "").strip()

        if book_id.isdigit():
            try:
                book = Books.objects.get(Book_id=int(book_id))

                if book.Quantity <= 0:
                    error = "This book is currently out of stock."

            except Books.DoesNotExist:
                error = "Book ID not found."
        else:
            error = "Please enter a valid Book ID."

    return render(request, "library_information/issue_book.html", {
        "book": book,
        "error": error,
        "book_id": book_id,
        "search_type": "book",
    })


# 3. Issue Book
def issue_book(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id", "").strip()
        book_id = request.POST.get("book_id", "").strip()

        if not student_id.isdigit() or not book_id.isdigit():
            messages.error(request, "Enter valid Student ID and Book ID.")
            return redirect("issue_book")

        try:
            with transaction.atomic():
                # Lock the book row while checking and updating stock
                book = Books.objects.select_for_update().get(
                    Book_id=int(book_id)
                )

                student = Student.objects.get(
                    Student_id=int(student_id)
                )

                # Only one active book per student
                already_issued = BookIssue.objects.filter(
                    Student=student,
                    Status="Issued"
                ).exists()

                if already_issued:
                    messages.error(
                        request,
                        "This student must return the current book before borrowing another."
                    )

                elif book.Quantity <= 0:
                    messages.error(
                        request,
                        "This book is out of stock."
                    )

                else:
                    BookIssue.objects.create(
                        Student=student,
                        Book=book,
                    )

                    book.Quantity -= 1
                    book.save(update_fields=["Quantity"])

                    messages.success(
                        request,
                        "Book issued successfully!"
                    )

        except Student.DoesNotExist:
            messages.error(request, "Student ID not found.")

        except Books.DoesNotExist:
            messages.error(request, "Book ID not found.")

        return redirect("issue_book")

    students = Student.objects.all()
    books = Books.objects.all()

    return render(request, "library_information/issue_book.html", {
        "students": students,
        "books": books,
    })


# 4. View Issued Books and Issue History
def issued_books(request):
    issues = BookIssue.objects.select_related("Student", "Book" ).order_by("-Issue_id")

    return render(request, "library_information/issued_books.html", { "issues": issues, })


# 5. Return Book
def return_book(request, issue_id):
    if request.method != "POST":
        return redirect("issued_books")

    try:
        with transaction.atomic():
            issue = BookIssue.objects.select_for_update().get(
                Issue_id=issue_id
            )

            if issue.Status == "Returned":
                messages.warning(
                    request,
                    "This book has already been returned."
                )
            else:
                book = Books.objects.select_for_update().get(
                    Book_id=issue.Book_id
                )

                issue.Status = "Returned"
                issue.Return_date = timezone.localdate()
                issue.save(update_fields=["Status", "Return_date"])

                book.Quantity += 1
                book.save(update_fields=["Quantity"])

                messages.success(
                    request,
                    "Book returned successfully!"
                )

    except BookIssue.DoesNotExist:
        messages.error(request, "Issue record not found.")

    return redirect("issued_books")