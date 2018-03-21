from django.shortcuts import  render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def login(request):
    c ={}
    c.update(csrf(request))
    return render_to_response('library/login.html',c)
def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/library/home/')
    else:
        c ={'error':"invalid"}
        c.update(csrf(request))
        return render_to_response('library/login.html',c)

@login_required(login_url='/accounts/login/')
def loggedin(request):
    return render_to_response('library/loggedin.html',{'full_name':request.user.username})


def invalid_login(request):
    c ={}
    c.update(csrf(request))
    return render_to_response('library/login.html',c)

@login_required(login_url='/accounts/login/')
def logout(request):
    auth.logout(request)
    c ={}
    c.update(csrf(request))
    return render_to_response('library/login.html',c)
