from django.urls import path
from recommend import views as recom
from home import views

urlpatterns = [
    path('', views.index, name='index'),

    path('upload/', views.importBookData, name='importBookData'),
    # path('hits_book/', views.hits_book, name='hits_book'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('register_conf_email/', views.register_conf_email, name='register_conf_email'),
    path('getbookinfo/<int:id>/', views.getBookInfo, name='getbookinfo'),
    path('bookpush/', recom.getRecommendBook, name='getrecommendbook'),
]
