from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql.functions import to_timestamp, col, when, avg
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('ConfirmationRate').getOrCreate()

signups_data = [
    (3, "2020-03-21 10:16:13"),
    (7, "2020-01-04 13:57:59"),
    (2, "2020-07-29 23:09:44"),
    (6, "2020-12-09 10:39:37")
]

signups_schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("time_stamp", StringType(), True)
])

signups_df = spark.createDataFrame(signups_data, signups_schema) \
    .withColumn("time_stamp", to_timestamp(col("time_stamp")))

signups_df.show()

confirmations_data = [
    (3, "2021-01-06 03:30:46", "timeout"),
    (3, "2021-07-14 14:00:00", "timeout"),
    (7, "2021-06-12 11:57:29", "confirmed"),
    (7, "2021-06-13 12:58:28", "confirmed"),
    (7, "2021-06-14 13:59:27", "confirmed"),
    (2, "2021-01-22 00:00:00", "confirmed"),
    (2, "2021-02-28 23:59:59", "timeout")
]

confirmations_schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("time_stamp", StringType(), True),
    StructField("action", StringType(), True)
])

confirmations_df = spark.createDataFrame(confirmations_data, confirmations_schema) \
    .withColumn("time_stamp", to_timestamp(col("time_stamp")))

confirmations_df.show()


confirmations_df.join(signups_df , on='user_id', how='left').select(
    signups_df.user_id,
    when(col('action')=='confirmed', 1).otherwise(0).alias('confirmation')
    ).groupBy('user_id')\
    .agg(
        round(avg(col('confirmation')), 2)\
        .alias('confirmation_rate')
    ).show()