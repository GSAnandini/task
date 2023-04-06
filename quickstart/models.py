from django.db import models

class User(models.Model):
    username = models.CharField(max_length=128,default='')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email
    

class Book(models.Model):
    name = models.CharField(max_length=50)


class BookIssue(models.Model):
    user = models.CharField(max_length=100,default='')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stat = models.CharField(max_length=150, default='')
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

