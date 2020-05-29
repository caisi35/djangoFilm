from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from authorize.views import index


urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^$', index, name='index'),
    url(r'home/', include('home.urls')),
    url(r'authorize/', include('authorize.urls')),
]
