from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

app_name='library_portal'
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^library/',include('library.urls')),
    #user auth urls
    url(r'^accounts/login/$', views.login),
    url(r'^accounts/auth/$', views.auth_view),
    url(r'^accounts/logout/$', views.logout),
    #url(r'^accounts/loggedin/$', views.loggedin),
    #url(r'^accounts/invalid/$', views.invalid_login),

]
