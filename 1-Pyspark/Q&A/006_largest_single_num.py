"""
https://github.com/rajeshreddy185/AzureDataEngineering-SQL/blob/main/19-LeetCodeQuestions/BiggestSingleNumber.md

"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, max
from pyspark.sql.types import StructType, StructField, IntegerType

num_data = [
    (8,),
    (8,),
    (3,),
    (3,),
    (1,),
    (4,),
    (5,),
    (6,)
]

num_schema = StructType([
    StructField("num", IntegerType(), True)
])
spark = SparkSession.builder.appName("LargesNum").getOrCreate()

num_df = spark.createDataFrame(num_data, num_schema)

num_df.show()


num_df.groupBy('num').agg(count('*').alias('each_count')).filter('each_count' == 1).agg(max('num'))
