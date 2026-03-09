from turtledemo.sorting_animate import partition

from pyspark.sql.functions import row_number
from pyspark.sql.types import StructType, StructField, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql import functions as F, Window

logs_data = [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 1),
    (6, 2),
    (7, 2)
]

logs_schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("num", IntegerType(), True)
])
spark = SparkSession.builder.appName('ConsecutiveNums').getOrCreate()

logs_df = spark.createDataFrame(logs_data, logs_schema)
a = logs_df.alias('a')
b = logs_df.alias('b')
c = logs_df.alias('c')

a.join(b, on=(a.id==b.id+1), how='inner').join(c,on=b.id+1==c.id+2, how='inner')\
.filter((a.num==b.num) & (b.num==c.num)).select(a.num).alias('num').show()


"""
OR
"""
window_spec = Window.orderBy(F.col('id'))
num_df = a.withColumn('next_num', F.lag('num').over(window_spec))\
    .withColumn('next_next_num', F.lag('num', 2).over(window_spec))
num_df.show()
num_df.filter((num_df.num == num_df.next_num) & (num_df.next_num == num_df.next_next_num)).show()


"""
OR
"""

window_spec = Window.orderBy(F.col('id'))
numb_df = a.withColumn('prev_num', F.lag('num', 1).over(window_spec))\
    .withColumn('prev_prev_num', F.lag('num', 2).over(window_spec))
num_df.filter((num_df.num == num_df.prev_num) & (num_df.prev_num == num_df.prev_prev_num)).show()