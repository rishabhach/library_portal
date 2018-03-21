from django.db import models
from django.core.urlresolvers import reverse
class Student(models.Model):
    first_name=models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    branch= models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    email = models.EmailField()
    roll_number=models.IntegerField()
    max_no_book_issue=models.IntegerField()
    number_of_issued_books=models.IntegerField(default=int(0))

    def get_absolute_url(self):
        return reverse('library:studentDetail',kwargs={'pk' :self.pk})


    def __str__(self):
        return (self.first_name+" "+self.last_name +" "+ str(self.roll_number)+" "+self.category+" "+str(self.max_no_book_issue))

class Book(models.Model):
    student = models.ForeignKey(Student,blank=True,null=True,default=None)
    title=models.CharField(max_length=50)
    book_id=models.CharField(max_length=10)
    author = models.CharField(max_length=50)
    publisher=models.CharField(max_length=50)
    edition=models.CharField(max_length=10)
    volume = models.IntegerField()
    book_type = models.CharField(max_length=20,default="TBB")
    price=models.IntegerField()

    def get_absolute_url(self):
        return reverse('library:bookDetail',kwargs={'pk' :self.pk})

    def __str__(self):
        return (self.title+" "+self.book_id)