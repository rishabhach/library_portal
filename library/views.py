from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from .forms import UserForm
from .models import Student, Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class StudentList(LoginRequiredMixin,generic.ListView):
    template_name = 'library/studentList.html'

    def get_queryset(self):
        return Student.objects.all()

class StudentDetail(LoginRequiredMixin,generic.DetailView):
    model = Student
    template_name = 'library/studentDetail.html'

class BookCreate(LoginRequiredMixin,generic.CreateView):
    model = Book
    fields = ['title','book_id','author','publisher','edition','price','volume','book_type']

class StudentCreate(LoginRequiredMixin,generic.CreateView):
    model = Student
    fields = ['first_name','last_name','branch','category','email','roll_number','max_no_book_issue','number_of_issued_books']

class Books(LoginRequiredMixin,generic.ListView):
    template_name = 'library/bookList.html'

    def get_queryset(self):
        return Book.objects.all()

class BookDetail(LoginRequiredMixin,generic.DetailView):
    model = Book
    template_name = 'library/bookDetail.html'

class UserFormView(View):
    form_class=UserForm
    template_name='library/registration_form.html'

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name,{'form':form})

    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False)

            username=form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            #returns user object if credentials are correct
            user=authenticate(username=username,password=password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect('library:students')
        return render(request, self.template_name, {'form': form})

@login_required(login_url='/accounts/login/')
def home(request):
    template=loader.get_template('library/index.html')
    return HttpResponse(template.render(None,request))

@login_required(login_url='/accounts/login/')
def bookstatus(request):
    template=loader.get_template('library/bookstatus.html')
    book = request.POST.get('Book')
    try:
        book_objects=Book.objects.filter(title=book)
    except:
        template = loader.get_template('library/index.html')
        context = {
            'error_message': "entered book detail is invalid, please enter a valid detail"}
        return HttpResponse(template.render(context, request))

    context={}
    if book_objects:
        context ={'book_object':book_objects}
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('library/index.html')
        context = {'error_message': "book does not exist, please enter a valid detail"}
        return HttpResponse(template.render(context,request))

@login_required(login_url='/accounts/login/')
def studentstatus(request):
    template = loader.get_template('library/studentstatus.html')
    roll_number = request.POST.get('roll_number')
    try:
        student=Student.objects.get(roll_number=roll_number)
        book_objects = Book.objects.filter(student__roll_number=roll_number)
    except:
        template = loader.get_template('library/index.html')
        context = {
            'error_message': "entered student details is invalid, please enter a valid detail"}
        return HttpResponse(template.render(context, request))

    
    context = {}
    if book_objects:
       context = {'book_objects': book_objects}
       return HttpResponse(template.render(context,request))
    else:
        template = loader.get_template('library/index.html')
        context = {'error_message': "No book found"}
        return HttpResponse(template.render(context, request))


@staff_member_required
@login_required(login_url='/accounts/login/')
def bookIssue(request):
    template = loader.get_template('library/bookIssue.html')
    return HttpResponse(template.render(None, request))


@staff_member_required
@login_required(login_url='/accounts/login/')
def bookIssueAuth(request):
    c={}
    bookId = request.POST.get('bookId','')
    studentRoll = request.POST.get('studentRoll','')
    try:
        book = Book.objects.get(book_id=bookId)
        student = Student.objects.get(roll_number=studentRoll)
    except :
        template = loader.get_template('library/bookIssue.html')
        c = {
            'error_message': "you entered wrong value"
        }
        return HttpResponse(template.render(c, request))
    if book.student is not None:
        template = loader.get_template('library/bookIssue.html')
        c = {
            'error_message': "book is already issued to someone"
        }
        return HttpResponse(template.render(c, request))
    if student.category=="SC" or student.category=="ST":
           if book.book_type=="SC/ST":
                if student.number_of_issued_books<5:
                           template = loader.get_template('library/bookDetail.html')
                           book.student=student
                           student.number_of_issued_books +=1
                           book.save()
                           student.save()
                           c = {
                           'book': book,
                                }
                           return HttpResponse(template.render(c, request))
                else:
                               template = loader.get_template('library/bookIssue.html')
                               c = {
                                   'error_message': "ypu have issued 5 books already"
                               }
                               return HttpResponse(template.render(c, request))
           elif book.book_type == "reading section":
                           template = loader.get_template('library/bookIssue.html')
                           c = {
                               'error_message': "sorry! this book belong to reading section. you cant issue it"
                           }
                           return HttpResponse(template.render(c, request))
           else:
                            template = loader.get_template('library/bookIssue.html')
                            c = {
                                'error_message': "book don't belong to your catagory"
                            }
                            return HttpResponse(template.render(c, request))
    elif student.category=="GENRAL" or student.category=="OBC":
            if book.book_type == "TBB":
                    if student.number_of_issued_books < 3:
                                template = loader.get_template('library/bookDetail.html')
                                book.student = student
                                student.number_of_issued_books += 1
                                book.save()
                                student.save()
                                c = {
                                    'book': book,
                                }
                                return HttpResponse(template.render(c, request))
                    else:
                                template = loader.get_template('library/bookIssue.html')
                                c = {
                                    'error_message': "ypu have issued 3 books already"
                                }
                                return HttpResponse(template.render(c, request))
            elif book.book_type == "reading section":
                            template = loader.get_template('library/bookIssue.html')
                            c = {
                                'error_message': "sorry! this book belong to reading section. you cant issue it"
                            }
                            return HttpResponse(template.render(c, request))
            else:
                            template = loader.get_template('library/bookIssue.html')
                            c = {
                                'error_message': "book don't belong to your catagory"
                            }
                            return HttpResponse(template.render(c, request))
    else:
                        template = loader.get_template('library/bookIssue.html')
                        c = {
                            'error_message': "there is some problem with this book please try again"
                        }
                        return HttpResponse(template.render(c, request))

@staff_member_required
@login_required(login_url='/accounts/login/')
def bookReturn(request):
    template = loader.get_template('library/bookreturn.html')
    return HttpResponse(template.render(None, request))


@staff_member_required
@login_required(login_url='/accounts/login/')
def bookReturnAuth(request):
    c = {}
    bookId = request.POST.get('bookId', '')
    try:
        book = Book.objects.get(book_id=bookId)
    except :
        template = loader.get_template('library/bookreturn.html')
        c = {
            'error_message': "you entered wrong value"
        }
        return HttpResponse(template.render(c, request))
    if book.student :
        student=book.student
        book.student=None
        book.save()
        student.number_of_issued_books-=1
        student.save()
        template = loader.get_template('library/studentDetail.html' )
        c={
           'student':student
            }
        return HttpResponse(template.render(c,request))
    else:
        template = loader.get_template('library/bookreturn.html')
        c = {
            'error_message': "book is not issued"
        }
        return HttpResponse(template.render(c, request))

@login_required(login_url='/accounts/login/')
def findBookdetail(request):
    template = loader.get_template('library/findBookDetail.html')
    return HttpResponse(template.render(None, request))

@login_required(login_url='/accounts/login/')
def findBookdetailAuth(request):
    c = {}
    bookId = request.POST.get('bookId', '')
    try:
        book_object = Book.objects.filter(book_id=bookId)
    except :
        template = loader.get_template('library/findBookDetail.html')
        c = {
            'error_message': "you entered wrong value"
        }
        return HttpResponse(template.render(c, request))
    if book_object:
        for book in book_object:
            template = loader.get_template('library/bookDetail.html')
            c = {
                'book': book,
            }
            return HttpResponse(template.render(c, request))
    else:
        template = loader.get_template('library/findBookDetail.html')
        c = {
            'error_message': "You Entered Wrong Book Detail"
        }
        return HttpResponse(template.render(c, request))

class BookUpdate(LoginRequiredMixin,UpdateView):
    model=Book
    fields=['title','book_id','author','publisher','edition','volume','book_type','price']

class BookDelete(LoginRequiredMixin,DeleteView):
    model=Book
    success_url=reverse_lazy('library:books')

@login_required(login_url='/accounts/login/')
def books_list(request):
    books = Book.objects.all()
    paginator = Paginator(books,10) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    return render(request, 'library/books_list.html', {'books': books})

@login_required(login_url='/accounts/login/')
def student_list(request):
    students = Student.objects.all()
    paginator = Paginator(students, 10) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)

    return render(request, 'library/student_list.html', {'students': students})


