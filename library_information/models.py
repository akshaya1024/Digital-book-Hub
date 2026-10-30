from django.db import models

# Create your models here.
class Books(models.Model):
    Book_id = models.AutoField(primary_key=True)
    Book_name = models.CharField(max_length=100, null=True)
    Author_name = models.CharField(max_length=100)
    Pubulished_date = models.DateField(auto_now_add=True)
    Quantity = models.IntegerField()

    def __str__(self):
        return self.Book_name

class Student(models.Model):
    Student_id = models.AutoField(primary_key=True)
    Student_name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    PhoneNo = models.CharField(max_length=10)
    Department = models.CharField(max_length=100)

    def __str__(self):
        return self.Student_name

from datetime import timedelta
from django.utils import timezone
from django.db import models


def calculate_due_date():
    return timezone.localdate() + timedelta(days=15)


class BookIssue(models.Model):
    Issue_id = models.AutoField(primary_key=True)

    Student = models.ForeignKey( Student, on_delete=models.CASCADE)

    Book = models.ForeignKey( Books, on_delete=models.CASCADE)

    Issue_date = models.DateField(auto_now_add=True)

    Due_date = models.DateField(default=calculate_due_date)

    Return_date = models.DateField(null=True, blank=True)

    Status = models.CharField( max_length=20, default="Issued")

    def __str__(self):
        return f"{self.Student.Student_name} - {self.Book.Book_name}"