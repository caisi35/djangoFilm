from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import os, csv
from djangoFilm import settings
from home.models import *
from recommend.recom import getRecommendByUserId
from django.contrib.auth.decorators import login_required
import threading
from django.db.models import Q


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
    if request.session.get('userid'):
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
    else:
        return redirect('login')


def split_page(object_list, request, per_page=20):
    """
    版权声明：本文为CSDN博主「Xyns」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/xinyan233/article/details/80236557
    :param object_list: 模型对象列表
    :param request:
    :param per_page: 一页的数量
    :return: 字典对象
    """
    paginator = Paginator(object_list, per_page)
    # 取出当前需要展示的页码, 默认为1
    page_num = request.GET.get('page', default='1')
    # 根据页码从分页器中取出对应页的数据
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger as e:
        # 不是整数返回第一页数据
        page = paginator.page('1')
        page_num = 1
    except EmptyPage as e:
        # 当参数页码大于或小于页码范围时,会触发该异常
        print('EmptyPage:{}'.format(e))
        if int(page_num) > paginator.num_pages:
            # 大于 获取最后一页数据返回
            page = paginator.page(paginator.num_pages)
        else:
            # 小于 获取第一页
            page = paginator.page(1)

    # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
    page_num = int(page_num)
    if page_num < 6:
        if paginator.num_pages <= 10:
            dis_range = range(1, paginator.num_pages + 1)
        else:
            dis_range = range(1, 11)
    elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
        dis_range = range(page_num - 5, page_num + 5)
    else:
        dis_range = range(paginator.num_pages - 9, paginator.num_pages + 1)

    data = {'page': page, 'paginator': paginator, 'dis_range': dis_range}
    return data


# 主页
def index(request):
    """
    # 分页： https://www.jianshu.com/p/332406309476
    # 加减： https://blog.csdn.net/qq_33472765/article/details/81174919
    :param request:
    :return:
    """
    if request.method == "GET":
        book_list = book.objects.order_by('rating').all()
        data = split_page(book_list, request)
        # locals()将所有变量传到templates
        return render(request, 'index.html', data)


# 启动预测推荐
def run_recommend(userid, rec_num=4):
    print('=================run_recommend===========================', userid)
    getRecommendByUserId(userid, rec_num)


# 用户登录
def login(request):
    if request.is_ajax():
        email = request.POST.get('email')
        password = request.POST.get('password')
        userEntry = user.objects.filter(email=email, password=password)
        if userEntry.exists():
            request.session['name'] = userEntry[0].name
            request.session['userid'] = userEntry[0].id
            data = {'code': 1}

            # 登录成功后，启用后台线程进行训练、预测
            t = threading.Thread(target=run_recommend, args=(userEntry[0].id, ), daemon=True)
            t.start()


        else:
            data = {'code': 0}
        return JsonResponse(data)
    return render(request, 'login.html')


# 用户退出登录
def logout(request):
    request.session.clear()
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
                password2) == 6:
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
    if request.session.get('userid'):
        userid = request.session.get('userid')
        bk = book.objects.get(id=id)
        currentuser = user.objects.get(id=userid)
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
        # user_id, book_id, hit_num
        data = str(currentuser.id) + ',' + str(id) + ',' + str(1)
        data2 = [str(currentuser.id), str(id), str(1)]
        print(data2)
        with open(r'/home/caisi/PycharmProjects/djangoFilm/recommend/data/hit.csv', 'a') as f:
            r = csv.writer(f)
            r.writerow(data2)
        return render(request, 'detail.html', locals())
    else:
        return redirect('login')

# 搜索视图
def search(request):
    kw = request.GET.get('kw')
    if kw:
        book_list = book.objects.filter(Q(name__icontains=kw) | Q(publish__icontains=kw))
        data = split_page(book_list, request)
        data['kw'] = kw
        # locals()将所有变量传到templates
        return render(request, 'search.html', data)
    else:
        kw = ''
        book_list = book.objects.order_by('-price').all()[0:40]
        data = split_page(book_list, request)
        data['kw'] = kw
        # locals()将所有变量传到templates
        return render(request, 'search.html', data)



