from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
from djangoFilm import settings
from home.models import *
from django.http import HttpResponse
import csv
from django.utils.deprecation import MiddlewareMixin
from utils import tools

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
    return render(request, 'upload.html')


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
            print('=====================hits_book=====================', e)
        return JsonResponse(data)


# 路由url白名单
WHITESITE = []


# 主页
def index(request):
    book_list = book.objects.all()
    user = request.session.get('user', None)
    userid = request.session.get('userid', None)

    # locals()将所有变量传到templates
    # print(type(book_list))
    # <class 'django.db.models.query.QuerySet'>
    return render(request, 'index.html', locals())


# 用户登录
def login(request):
    if request.is_ajax():
        email = request.POST.get('email')
        password = request.POST.get('password')
        userEntry = user.objects.filter(email=email, password=password)
        print(email, password, '=========================')
        if userEntry.exists():
            request.session['name'] = userEntry[0].name
            request.session['userid'] = userEntry[0].id
            print('True')
            data = {'code': 1}
        else:
            print('False')
            data = {'code': 0}
        return JsonResponse(data)
    return render(request, 'login.html')


# https://blog.csdn.net/piduocheng0577/article/details/105031958
class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in WHITESITE or str(request.path_info).startswith('/admin'):
            print(request.path_info)
        elif request.session.get('user', None):
            print(request.path_info)
        else:
            return redirect('login')


# 用户退出登录
def logout(request):
    request.session.flush()
    return redirect('index')


# 注册
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # 确认密码和没有相同的邮箱
        if password == password2 and not user.objects.filter(email=email).exists() and password2 is not '' and len(
                password2)==6:
            userEntry = user(email=email, name=name, password=password)
            userEntry.save()
            return redirect('login')
        else:
            return render(request, 'register.html', {'msg': '注册失败，请重试！'})
    return render(request, 'register.html')


# 用户是否存在
def register_conf_email(request):
    """
    ajax 传注册的email验证是否已经存在
    :param request:
    :return: 存在返回True，否在返回False
    """
    email = request.POST.get('email')
    result = user.objects.filter(email=email)
    if result.exists():
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})


# 获取图书详情
def getBookInfo(request, id):
    bk = book.objects.get(id=id)
    userid = request.session.get('userid', None)
    currentuser = user.objects.get(id=userid)
    # 1
    # id: 1
    # 啊啊啊
    # print(currentuser)
    try:
        hit = hits.objects.get(userid=currentuser.id, bookid=id)
        hit.hitnum += 1
        hit.save()
    except:
        hit = hits()
        hit.bookid = id
        hit.hitnum = 1
        hit.userid = currentuser.id
        hit.save()
    data = str(currentuser.id) + ',' + str(id) + ',' + str(1)
    return render(request, 'detail.html', locals())


import redis

pool = redis.ConnectionPool(host='localhost', port=6379)
redis_client = redis.Redis(connection_pool=pool)


def getRecommendBook(request):
    userid = request.GET.get('userid')
    recommendbook = redis_client.get(int(userid))
    booklist = str(recommendbook).split('|')
    bookset = []
    for bk in booklist[:-1]:
        bookid = bk.split(',')[-1]
        bk_entry = book.objects.get(id=bookid)
        bookset.append(bk_entry)
    return render(request, 'recommend.html', locals())
