from django.conf.urls import url
from authorize.views import *

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^register_conf_email/$', register_conf_email, name='register_conf_email'),
    url(r'^getbookinfo/$', getBookInfo, name='getbookinfo'),
    url(r'^bookpush/$', getRecommendBook, name='getrecommendbook'),
]
