from django.shortcuts import render
import os
from djangoFilm import settings
from .models import book
from django.http import HttpResponse
# Create your views here.


def handle_upload_file(name, file):
    path = os.path.join(settings.BASE_DIR, 'uploads')
    fileName = path+'/'+name
    with open(fileName, 'web') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    insertToSQL(fileName)


def insertToSQL(fileName):
    txtfile = open(fileName, 'r')
    for line in txtfile.readline():
        try:
            bookinfo = line.split(',')
            id = bookinfo[0].decode().encode('utf-8')
            name = bookinfo[1].decode().encode('utf-8')
            rating = bookinfo[2].decode().encode('utf-8')
            price = bookinfo[3].decode().encode('utf-8')
            publish = bookinfo[4].decode().encode('utf-8')
            url = bookinfo[5].decode().encode('utf-8')
            try:
                bk_entry= book(name=name, price=price, url=url,publish=publish,rating=rating)
                bk_entry.save()
            except:
                print('save error'+id)
        except:
            print('read error'+id)


def importBookData(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        if not file:
            return HttpResponse('success')
    return render(request, 'utils/upload.html')