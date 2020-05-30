from django.shortcuts import render, redirect
from home.models import book
import redis
from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext
from pyspark.mllib.recommendation import ALS

pool = redis.ConnectionPool(host='localhost', port=6379)
redis_client = redis.Redis(connection_pool=pool)


def getRecommendByUserId(userid, rec_num):
    """
    :param userid: 用户id
    :param rec_num: 推荐数量
    :return:
    """
    sc = SparkContext(master='local[4]')
    sql_content = SQLContext(sc)
    read = sql_content.read
    df = read.schema('user_id Int, book_id Int, hit_num Int').csv(path='./recommend/data/hit.csv')
    df.registerTempTable('hit')
    sqlContext = SparkSession.builder.getOrCreate()
    data = sqlContext.sql('select user_id,book_id,sum(hit_num) as hits from hit group by user_id, book_id')
    bookrdd = data.rdd.map(lambda x: (x.user_id, x.book_id, x.hits))
    model = ALS.trainImplicit(bookrdd, 10, 10, 0.01)
    try:
        result = model.recommendProducts(userid, rec_num)
        temp = ''
        for r in result:
            temp += str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + '|'
        redis_client.set(userid, temp)
        print(result)
        print('load model success !')
    except Exception as e:
        print('load model failed!====================================\n' + str(e))
    sc.stop()


def getRecommendBook(request):
    userid = request.session.get('userid')
    if userid:
        getRecommendByUserId(userid, 4)
        recommendbook = redis_client.get(int(userid))
        booklist = str(recommendbook).split('|')
        bookset = []
        for bk in booklist[:-1]:
            bookid = bk.split(',')[1]
            bk_entry = book.objects.get(id=bookid)
            bookset.append(bk_entry)

        return render(request, 'recommend.html', locals())
    else:
        redirect('login')