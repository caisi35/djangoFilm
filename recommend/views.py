from django.shortcuts import render, redirect
from home.models import book
import redis


pool = redis.ConnectionPool(host='localhost', port=6379)
redis_client = redis.Redis(connection_pool=pool)


def getRecommendBook(request):
    userid = request.session.get('userid')
    if userid:
        # 推荐图书
        # model.getRecommendByUserId()

        recommendbook = redis_client.get(int(userid))
        booklist = str(recommendbook).split('|')
        bookset = []
        for bk in booklist[:-1]:
            bookid = bk.split(',')[1]
            bk_entry = book.objects.get(id=bookid)
            bookset.append(bk_entry)

        return render(request, 'recommend.html', locals())
    else:
        return redirect('login')


