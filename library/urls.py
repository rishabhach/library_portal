from django.conf.urls import url
from . import views
from django.contrib.admin.views.decorators import staff_member_required

app_name='library'

urlpatterns=[
    # url(r'^$',views.index,name='index'),
    url(r'^register/$' ,staff_member_required(views.UserFormView.as_view()) ,name='register'),
    url(r'^students/$' ,views.StudentList.as_view() ,name='students'),
    url(r'^students/(?P<pk>[0-9]+)/$' ,views.StudentDetail.as_view() ,name='studentDetail'),
    url(r'^books/$' , views.Books.as_view() ,name='books'),
    url(r'^books/(?P<pk>[0-9]+)/$' , views.BookDetail.as_view() , name='bookDetail'),
    url(r'^addbook/$' , staff_member_required(views.BookCreate.as_view()) , name='AddBook'),
    url(r'^addstudent/$' , staff_member_required(views.StudentCreate.as_view()) , name='Addstudent'),
    url(r'^home/$' , views.home,name='index'),
    url(r'^bookstatus/$' , views.bookstatus),
    url(r'^studentstatus/$' , views.studentstatus) ,
    url(r'^bookIssue/$' , views.bookIssue, name='BookIssue') ,
    url(r'^BookIssueAuth/$' , views.bookIssueAuth , name= 'BookIssueAuth') ,
    url(r'^returnbook/$' , views.bookReturn , name='ReturnBook'),
    url(r'^bookReturnAuth/$' , views.bookReturnAuth , name='bookReturnAuth'),
    url(r'^findBookdetail/$' , views.findBookdetail , name='findBookdetail'),
    url(r'^findBookdetailAuth/$', views.findBookdetailAuth, name='findBookdetailAuth'),
    url(r'^update/(?P<pk>[0-9]+)/$', staff_member_required(views.BookUpdate.as_view()), name='BookUpdate'),
    url(r'^books/(?P<pk>[0-9]+)/delete/$' , staff_member_required(views.BookDelete.as_view()) , name='BookDelete'),
    url(r'^book_list/$' , views.books_list ,name='books_test'),
    url(r'^student_list/$' , views.student_list ,name='student_test'),
]