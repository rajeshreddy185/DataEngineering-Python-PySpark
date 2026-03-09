from pyspark.sql.types import StructType, StructField, IntegerType, StringType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, max

employee_data = [
    (3, "Brad", None, 4000),
    (1, "John", 3, 1000),
    (2, "Dan", 3, 2000),
    (4, "Thomas", 3, 4000)
]

employee_schema = StructType([
    StructField("empId", IntegerType(), True),
    StructField("name", StringType(), True),
    StructField("supervisor", IntegerType(), True),
    StructField("salary", IntegerType(), True)
])

spark = SparkSession.builder.appName("EmpBonus").getOrCreate()
employee_df = spark.createDataFrame(employee_data, employee_schema)

employee_df.show()

bonus_data = [
    (2, 500),
    (4, 2000)
]

bonus_schema = StructType([
    StructField("empId", IntegerType(), True),
    StructField("bonus", IntegerType(), True)
])

bonus_df = spark.createDataFrame(bonus_data, bonus_schema)

bonus_df.show()

employee_df.join(bonus_df, on='empId', how='left').filter(bonus_df.bonus < 1000).select(bonus_df.empId, bonus_df.bonus).show()



