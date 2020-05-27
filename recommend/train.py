from pyspark import SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.ml.recommendation import ALS

sc = SparkContext()
txt = sc.textFile('file:///home/hit.txt')
ratingsRDD = txt.flatMap(lambda x:x.split()).map(lambda x:x.split(','))
sqlContext = SparkSession.builder.getOrCreate()
user_row = ratingsRDD.map(lambda x:Row(userid=int(x=[0]),bookid=int(x[1]),hitnum=int(x[2])))
user_df = sqlContext.createDataFrame(user_row)
user_df.registerTempTable('test')
datatable = sqlContext.sql('select userid, bookid, sum(hitnum) as hitnum from test group by userid, bookid')
bookrdd = datatable.rdd.map(lambda x:(x.userid, x.bookid, x.hitnum))
model = ALS.trainImplicit(bookrdd,10,10,0.01)
import os
import shutil
if os.path.exists('recommendModel'):
    shutil.rmtree('recommemdModel')
model.save(sc, 'recommemdModel')

