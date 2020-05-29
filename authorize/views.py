from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from home.models import book, hits
from authorize.models import user
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

# from utils import tools
# Create your views here.


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
    return render(request, 'home/index.html', locals())


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
    return render(request, 'auth/login.html')


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info in WHITESITE or str(request.path_info).startswith('/admin'):
            print(request.path_info)
        elif request.session.get('user', None):
            print(request.path_info)
        else:
            return HttpResponseRedirect('/login/')


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
            return render(request, 'auth/register.html', {'msg': '注册失败，请重试！'})
    return render(request, 'auth/register.html')


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


def getBookInfo(request):
    id = request.GET.get('id')
    bk = book.objects.get(id=id)
    username = request.session.get('user', None)
    currentuser = user.objects.get(name=username)
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
    # tools.
    return render(request, 'home/detail.html', locals())


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
    return render(request, 'auth/recommend.html', locals())
