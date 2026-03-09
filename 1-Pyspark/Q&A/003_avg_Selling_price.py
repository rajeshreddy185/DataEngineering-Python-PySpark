"""
Question Link:
https://github.com/rajeshreddy185/AzureDataEngineering-SQL/blob/main/19-LeetCodeQuestions/AverageSellingPrice.md
"""

from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, DateType, StringType
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date, col, sum, round

spark = SparkSession.builder.appName("Products").getOrCreate()

prices_data = [
    (1, "2019-02-17", "2019-02-28", 5.00),
    (1, "2019-03-01", "2019-03-22", 20.00),
    (2, "2019-02-01", "2019-02-20", 15.00),
    (2, "2019-02-21", "2019-03-31", 30.00)
]

prices_schema = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("start_date", StringType(), True),
    StructField("end_date", StringType(), True),
    StructField("price", DoubleType(), True)
])

prices_df = spark.createDataFrame(prices_data, prices_schema) \
    .withColumn("start_date", to_date(col("start_date"))) \
    .withColumn("end_date", to_date(col("end_date")))

prices_df.show()


units_data = [
    (1, "2019-02-25", 100),
    (1, "2019-03-01", 15),
    (2, "2019-02-10", 200),
    (2, "2019-03-22", 30)
]

units_schema = StructType([
    StructField("product_id", IntegerType(), True),
    StructField("purchase_date", StringType(), True),
    StructField("units", IntegerType(), True)
])

units_df = spark.createDataFrame(units_data, units_schema) \
    .withColumn("purchase_date", to_date(col("purchase_date")))

units_df.show()


df = prices_df.join(
    units_df,
    prices_df.product_id == units_df.product_id
).filter(
    col("purchase_date").between(col("start_date"), col("end_date"))
).select(
    prices_df.product_id,
    (prices_df.price * units_df.units).alias("total_selling_price"),
    units_df.units
)

result = df.groupBy("product_id").agg(
    round(
        sum("total_selling_price") / sum("units"),
        2
    ).alias("avg_price")
)

result.show()