from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("SplBonus").getOrCreate()

employee_data = [
    (2, "Meir", 3000),
    (3, "Michael", 3800),
    (7, "Addilyn", 7400),
    (8, "Juan", 6100),
    (9, "Kannon", 7700)
]

employee_schema = StructType([
    StructField("employee_id", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("salary", IntegerType(), True)
])

employee_df = spark.createDataFrame(employee_data, employee_schema)

employee_df.show()

bonus_data = [
    (2, 0),
    (3, 0),
    (7, 7400),
    (8, 0),
    (9, 7700)
]

bonus_schema = StructType([
    StructField("employee_id", IntegerType(), True),
    StructField("bonus", IntegerType(), True)
])

bonus_df = spark.createDataFrame(bonus_data, bonus_schema)

bonus_df.show()


employee_df.select(
    F.col('employee_id'),
    F.when(
            (~F.col('name').startswith('M')) & (F.col('employee_id')%2==0),
           F.col('salary')).otherwise(0).alias('bonus')
).show()