"""
https://github.com/rajeshreddy185/AzureDataEngineering-SQL/blob/main/19-LeetCodeQuestions/AverateTimeperMachinetoProcess.md
"""


from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
from pyspark.sql import SparkSession
from pyspark.sql import functions as f

spark = SparkSession.builder.appName("ActivityTable").getOrCreate()

activity_data = [
    (0, 0, "start", 0.712),
    (0, 0, "end", 1.520),
    (0, 1, "start", 3.140),
    (0, 1, "end", 4.120),
    (1, 0, "start", 0.550),
    (1, 0, "end", 1.550),
    (1, 1, "start", 0.430),
    (1, 1, "end", 1.420),
    (2, 0, "start", 4.100),
    (2, 0, "end", 4.512),
    (2, 1, "start", 2.500),
    (2, 1, "end", 5.000)
]

activity_schema = StructType([
    StructField("machine_id", IntegerType(), True),
    StructField("process_id", IntegerType(), True),
    StructField("activity_type", StringType(), True),
    StructField("timestamp", DoubleType(), True)
])

activity_df = spark.createDataFrame(activity_data, activity_schema)

activity_df.show()

activity_df.groupBy('machine_id').agg(
    (
        f.round(
        f.sum(
            f.when(
                activity_df.activity_type == 'end', activity_df.timestamp
            ).otherwise(0).alias('end_time')
        )
        -
        f.sum(
            f.when(
                activity_df.activity_type == 'start', activity_df.timestamp
            ).otherwise(0).alias('start_time')
        )/ f.countDistinct('activity_type')
    ,3)
    ).alias('average_time')
).show()