from django.shortcuts import render
from django.http import JsonResponse
import os
from djangoFilm import settings
from home.models import book, hits
from django.http import HttpResponse
import csv


# 将上传的文件保存到本地
def handle_upload_file(name, file):
    """
    将上传的文件保存到服务器的uploads文件夹下，并调用insertToSQL函数
    :param name: 文件名
    :param file: 文件对象
    """
    path = os.path.join(settings.BASE_DIR, 'uploads')
    fileName = path + '/' + name
    # fileName /home/caisi/PycharmProjects/djangoFilm/uploads/GoodBooks.csv
    # print('fileName', fileName)
    with open(fileName, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    insertToSQL(fileName)


# 打开上传到本地的文件，并写入数据库
def insertToSQL(fileName):
    # # <_io.TextIOWrapper name='/home/caisi/PycharmProjects/djangoFilm/uploads/GoodBooks.csv' mode='r' encoding='UTF-8'>
    # # print(txtfile)
    with open(fileName, 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        # count:55344
        for bookinfo in data:
            try:
                id = bookinfo[0]
                name = bookinfo[1]
                rating = bookinfo[2]
                price = float(bookinfo[3])
                publish = bookinfo[4]
                url = bookinfo[5]
                try:
                    bk_entry = book(name=name, price=price, url=url, publish=publish, rating=rating)
                    bk_entry.save()
                except Exception as e:
                    print('*********************save error*********************save error' + id + str(e))
            except Exception as e:
                print('=====================read error======================' + bookinfo[0] + str(e))


# 上传文件
def importBookData(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        if not file:
            return HttpResponse('None File uploads ! ')
        else:

            name = file.name
            # name GoodBooks.csv file type <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
            # print('name',name, 'file type', type(file))
            handle_upload_file(name, file)
            return HttpResponse('success')
    return render(request, 'utils/upload.html')


# 点击量
def hits_book(request):
    if request.is_ajax():
        book_id = request.POST.get('book_id')
        user_id =request.POST.get('user_id')

        try:
            hit = hits.objects.get(bookid=book_id, userid=user_id)
            hit.hitnum += 1
            hit.save()
            data = {'result': True}
        except Exception as e:
            hit = hits()
            hit.bookid = book_id
            hit.hitnum = 1
            hit.userid = user_id
            hit.save()
            data = {'result': False}
            print(e)
        return JsonResponse(data)
