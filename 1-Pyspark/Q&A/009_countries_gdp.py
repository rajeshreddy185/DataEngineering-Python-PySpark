from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType
from pyspark.sql import SparkSession, functions as F

world_data = [
    ("Afghanistan", "Asia", 652230, 25500100, 20343000000),
    ("Albania", "Europe", 28748, 2831741, 12960000000),
    ("Algeria", "Africa", 2381741, 37100000, 188681000000),
    ("Andorra", "Europe", 468, 78115, 3712000000),
    ("Angola", "Africa", 1246700, 20609294, 100990000000)
]

world_schema = StructType([
    StructField("name", StringType(), True),
    StructField("continent", StringType(), True),
    StructField("area", IntegerType(), True),
    StructField("population", IntegerType(), True),
    StructField("gdp", LongType(), True)
])
spark = SparkSession.builder.appName('CountryGDP').getOrCreate()
world_df = spark.createDataFrame(world_data, world_schema)

world_df.show()

world_df.filter((F.col('area') >= 30000000)| (F.col('gdp') >= 255000000))