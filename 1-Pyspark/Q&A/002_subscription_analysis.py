"""

Question Link
https://github.com/rajeshreddy185/AzureDataEngineering-SQL/blob/main/19-LeetCodeQuestions/AnalyseSubscriptionConversion.md

"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date
from pyspark.sql.types import StructType, StructField, IntegerType, DateType, StringType

# Create SparkSession
spark = SparkSession.builder \
    .appName("SubscriptionConversion") \
    .getOrCreate()

# Schema using StructField
schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("activity_date", StringType(), True),
    StructField("activity_type", StringType(), True),
    StructField("activity_duration", IntegerType(), True)
])



data = [
    (1, "2023-01-01", "free_trial", 45),
    (1, "2023-01-02", "free_trial", 30),
    (1, "2023-01-05", "free_trial", 60),
    (1, "2023-01-10", "paid", 75),
    (1, "2023-01-12", "paid", 90),
    (1, "2023-01-15", "paid", 65),
    (2, "2023-02-01", "free_trial", 55),
    (2, "2023-02-03", "free_trial", 25),
    (2, "2023-02-07", "free_trial", 50),
    (2, "2023-02-10", "cancelled", 0),
    (3, "2023-03-05", "free_trial", 70),
    (3, "2023-03-06", "free_trial", 60),
    (3, "2023-03-08", "free_trial", 80),
    (3, "2023-03-12", "paid", 50),
    (3, "2023-03-15", "paid", 55),
    (3, "2023-03-20", "paid", 85),
    (4, "2023-04-01", "free_trial", 40),
    (4, "2023-04-03", "free_trial", 35),
    (4, "2023-04-05", "paid", 45),
    (4, "2023-04-07", "cancelled", 0)
]

# Create DataFrame
df = spark.createDataFrame(data, schema)

# Convert date column
df = df.withColumn("activity_date", to_date(col("activity_date")))

df.show()

print("DataFrame Schema:")
df.printSchema()

# Basic analysis
print("Activity types distribution:")
df.groupBy("activity_type").count().show()

# User-level analysis
from pyspark.sql.functions import sum as _sum, avg as _avg, count as _count, when

print("User activity summary:")
user_summary = df.groupBy("user_id").agg(
    _count("*").alias("total_activities"),
    _sum("activity_duration").alias("total_duration"),
    _count(when(col("activity_type") == "free_trial", True)).alias("free_trial_days"),
    _count(when(col("activity_type") == "paid", True)).alias("paid_days"),
    _count(when(col("activity_type") == "cancelled", True)).alias("cancelled_days")
)
user_summary.show()

# Conversion analysis - users who converted from free_trial to paid
print("Users who converted from free trial to paid:")
free_trial_users = df.filter(col("activity_type") == "free_trial").select("user_id").distinct()
paid_users = df.filter(col("activity_type") == "paid").select("user_id").distinct()
converted_users = free_trial_users.join(paid_users, "user_id", "inner")
converted_users.show()

print(f"Total users who converted: {converted_users.count()}")

# Users who cancelled
print("Users who cancelled:")
cancelled_users = df.filter(col("activity_type") == "cancelled").select("user_id").distinct()
cancelled_users.show()

print(f"Total users who cancelled: {cancelled_users.count()}")

# Conversion rate
total_free_trial_users = free_trial_users.count()
conversion_rate = (converted_users.count() / total_free_trial_users) * 100 if total_free_trial_users > 0 else 0
print(f"Conversion rate: {conversion_rate:.2f}%")

# Stop SparkSession
spark.stop()
