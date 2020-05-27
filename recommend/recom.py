import redis
from pyspark import SparkContext
from pyspark.mllib.recommendation import MatrixFactorizationModel


pool = redis.ConnectionPool(host='localhost', port=6379)
redis_client = redis.Redis(connection_pool=pool)
sc = SparkContext("spark://home/caisi/PycharmProjects/djangoFilm", "recommend")


def getRecommendByUserId(userid, rec_num):
    try:
        model = MatrixFactorizationModel.load(sc, 'recommendModel')
        result = model.recommendProducts(userid, rec_num)
        temp=''
        for r in result:
            temp+=str(r[0])+','+str(r[1])+','+str(r[2])+'|'
        redis_client.set(userid, temp)
        print('load model success !')
    except Exception as e:
        print('load model failed!' + str(e))
    sc.stop()