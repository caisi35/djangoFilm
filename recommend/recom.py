import redis
from pyspark import SparkContext
from pyspark.mllib.recommendation import MatrixFactorizationModel


def getRecommendByUserId(userid, rec_num):
    """
    :param userid: 用户id
    :param rec_num: 推荐数量
    """
    try:
        pool = redis.ConnectionPool(host='localhost', port=6379)
        redis_client = redis.Redis(connection_pool=pool)
        sc = SparkContext()

        # 加载模型
        model = MatrixFactorizationModel.load(sc, 'recommend/recommemdModel')
        # 预测
        result = model.recommendProducts(userid, rec_num)
        temp = ''
        for r in result:
            temp += str(r[0]) + ',' + str(r[1]) + ',' + str(r[2]) + '|'
        # 将结果保存到内存数据库
        redis_client.set(userid, temp)
        print('load model success!\n')
    except Exception as e:
        print('load model failed!\n' + str(e))
    sc.stop()


if __name__ == '__main__':
    getRecommendByUserId(2,4)
