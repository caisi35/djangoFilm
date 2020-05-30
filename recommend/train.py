from pyspark import SparkContext
from pyspark.sql import SparkSession, SQLContext
from pyspark.mllib.recommendation import ALS
import os
import shutil

sc = SparkContext()
sql_content = SQLContext(sc)
read = sql_content.read
df = read.schema('user_id Int, book_id Int, hit_num Int').csv(path='./data/hit.csv')
df.registerTempTable('hit')
sqlContext = SparkSession.builder.getOrCreate()
data = sqlContext.sql('select user_id,book_id,sum(hit_num) as hits from hit group by user_id, book_id')
# data.show()
# +-------+-------+-------+
# |user_id|book_id|hit_num|
# +-------+-------+-------+
# |      1|      1|      1|
# |      1|      4|      1|
# +-------+-------+-------+

bookrdd = data.rdd.map(lambda x: (x.user_id, x.book_id, x.hits))

model = ALS.trainImplicit(bookrdd, 10, 10, 0.01)


if os.path.exists('recommendModel'):
    shutil.rmtree('recommemdModel')
model.save(sc, 'recommemdModel')
