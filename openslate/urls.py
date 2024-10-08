"""openslate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

from user import views
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),

#    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='logout'),
    
    path('adminlogin/', LoginView.as_view(template_name='user/adminlogin.html'), name='adminlogin'),
#    path('studentlogin', LoginView.as_view(template_name='user/studentlogin.html'), name='studentlogin'),
#    path('logout', LogoutView.as_view(template_name='user/index.html')),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True), name='favicon'),

    path('studentlogin/', views.CustomLoginView.as_view(), name='studentlogin'),
    path('studentlogout/', views.CustomLogoutView.as_view(), name='studentlogout'),


   
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    


    


