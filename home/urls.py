from django.conf.urls import url
from home.views import importBookData, hits_book

urlpatterns = [
    url(r'^upload/$', importBookData, name='importBookData'),
    url(r'^hits_book/', hits_book, name='hits_book'),
]
