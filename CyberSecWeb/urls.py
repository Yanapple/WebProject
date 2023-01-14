"""CyberSecWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))python
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from application.views import index_page, main_page, geography_page, availability_page, skills_page, vacation_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main', main_page, name='main_page'),
    path('geography', geography_page, name='geography'),
    path('availability', availability_page, name='availability'),
    path('skills', skills_page, name='skills'),
    path('vacation', vacation_page, name='vacation'),
    path('', index_page), #путь для главной страницы
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)