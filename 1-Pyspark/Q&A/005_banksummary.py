from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("BankTables").getOrCreate()

users_data = [
    (900001, "Alice"),
    (900002, "Bob"),
    (900003, "Charlie")
]

users_schema = StructType([
    StructField("account", IntegerType(), True),
    StructField("name", StringType(), True)
])

users_df = spark.createDataFrame(users_data, users_schema)

users_df.show()

from pyspark.sql.types import DoubleType, DateType
from pyspark.sql.functions import to_date, col

transactions_data = [
    (1, 900001, 7000, "2020-08-01"),
    (2, 900001, 7000, "2020-09-01"),
    (3, 900001, -3000, "2020-09-02"),
    (4, 900002, 1000, "2020-09-12"),
    (5, 900003, 6000, "2020-08-07"),
    (6, 900003, 6000, "2020-09-07"),
    (7, 900003, -4000, "2020-09-11")
]

transactions_schema = StructType([
    StructField("trans_id", IntegerType(), True),
    StructField("account", IntegerType(), True),
    StructField("amount", IntegerType(), True),
    StructField("transacted_on", StringType(), True)
])

transactions_df = spark.createDataFrame(transactions_data, transactions_schema) \
    .withColumn("transacted_on", to_date(col("transacted_on")))

transactions_df.show()

transactions_df.groupBy("account")\
    .agg(F.sum("amount").alias('total_amount'))\
    .filter(F.col('total_amount') > 10000) \
    .join(users_df, on='account', how='inner')\
    .show()