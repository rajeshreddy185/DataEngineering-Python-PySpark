"""
You receive daily transaction logs (CSV) with:
Tasks
1. Load the CSV into PySpark with an explicit schema
2. Remove duplicate transactions
3. Filter out records where amount <= 0
4. Convert transaction_timestamp to proper timestamp format
5. Calculate total debit and credit amount per day
6. Store the result in Parquet format partitioned by date


Schema:
- transaction_id (string)
- user_id (string)
- amount (double)
- transaction_type (string: credit/debit)
- transaction_timestamp (string)

"""

from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


spark = SparkSession.builder.appName('TransactionCleanup').getOrCreate()

schema = StructType([
    StructField('transaction_id', StringType(), True),
    StructField('user_id', StringType(), True),
    StructField('amount', DoubleType(), True),
    StructField('transaction_type', StringType(), True),
    StructField('transaction_timestamp', StringType(), True)

])


total_records = 1000
num_partitions = 10

df = spark.range(10, total_records,numPartitions=num_partitions)

fake_payments_df = df.select(

    F.expr("uuid()").alias("transaction_id"),
    F.concat(F.lit("user_"), F.floor(F.rand()*50).cast("int")).alias("user_id"),
    F.round(F.rand()*10000, 2).alias("amount"),
    F.when(F.rand() < 0.7, F.lit("debit"))
     .otherwise(F.lit("credit"))
     .alias("transaction_type"),

    (F.unix_timestamp()).cast('long')
        .alias("transaction_timestamp")

)

fake_payments_df.show(30, False)




# MAGIC %md
# MAGIC Convert transaction_timestamp to proper timestamp format



payment_df = fake_payments_df.withColumn('transaction_date', F.to_date(F.col('transaction_timestamp').cast('timestamp')))
payment_df.show()



# MAGIC %md
# MAGIC Remove duplicate transactions



from pyspark.sql.window import Window

window_spec = Window.partitionBy('transaction_id').orderBy('transaction_timestamp')

ranked_df = payment_df.withColumn('rank', F.row_number().over(window_spec))

ranked_df.show()





ranked_df.filter(F.col('rank') == 1).show()
ranked_df.show()



# MAGIC %md
# MAGIC  Filter out records where amount <= 0



amnt_filtered_df = ranked_df.filter(F.col('amount') > 1)
amnt_filtered_df.filter(F.col('user_id') == 'user_1').show()



# MAGIC %md
# MAGIC Calculate total debit and credit amount per day



seggregated_amnt = amnt_filtered_df.groupBy('user_id', 'transaction_type').agg(F.round(F.sum('amount'),2).alias('amount'))
seggregated_amnt.show()




report_data = seggregated_amnt.groupBy('user_id').agg(
    (
        F.sum(
            F.when(
                F.col('transaction_type')=='debit', F.col('amount')
                ).otherwise(0)
        )
    ).alias('total_debit_amount'),
    (
        F.sum(
            F.when(
                F.col('transaction_type')=='credit', F.col('amount')
                ).otherwise(0)
        )
    ).alias('total_credit_amount')
)

report_data.show()



# MAGIC %md
# MAGIC Write to Parquet Partitioned by Date



report_data.write \
    .mode("overwrite") \
    .partitionBy("transaction_date") \
    .parquet("path/to/output/")