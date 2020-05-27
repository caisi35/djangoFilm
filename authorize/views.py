from django.shortcuts import render
from .models import user, book, hits
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
# from utils import tools
# Create your views here.


# 路由url白名单
WHITESITE = ["/login/",]


# 用户登录
def login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        userEntry = user.objects.filter(name=name, password=password)
        if userEntry.exists():
            request.session['user'] = name
            request.session['userid'] = userEntry[0].id
            return HttpResponse('/')
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
    request.session().clear()
    return HttpResponse('Exit')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        userEntry = user(name=name, password=password)
        userEntry.save()
        return HttpResponseRedirect('auth/login.html')
    return render(request, 'auth/register.html', locals())


def getBookInfo(request):
    id = request.GET.get('id')
    bk = book.objects.get(id=id)
    username = request.session.get('user', None)
    currentuser = user.objects.get(name=username)
    try:
        hit = hits.objects.get(userid=currentuser.id, bookid=id)
        hit.hitnum +=1
        hit.save()
    except:
        hit = hits()
        hit.bookid = id
        hit.hitnum = 1
        hit.userid = currentuser.id
        hit.save()
    data = str(currentuser.id)+','+str(id)+','+str(1)
    # tools.
    return render(request, 'home/detail.html', locals())


def index(request):
    book_list = book.objects.all()
    user = request.session.get('user', None)
    userid = request.session.get('userid', None)
    test = 'test'
    # locals()将所有变量传到templates
    return render(request, 'home/index.html', locals())


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
