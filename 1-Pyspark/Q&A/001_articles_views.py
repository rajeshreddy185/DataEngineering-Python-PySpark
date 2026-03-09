"""
Question Link:
https://github.com/rajeshreddy185/AzureDataEngineering-SQL/blob/main/19-LeetCodeQuestions/AutorandViewer.md
"""


from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, IntegerType, DateType

# Create SparkSession
spark = SparkSession.builder \
    .appName("ArticlesViews") \
    .getOrCreate()

# Define schema for the articles views table
schema = StructType([
    StructField("article_id", IntegerType(), True),
    StructField("author_id", IntegerType(), True),
    StructField("viewer_id", IntegerType(), True),
    StructField("view_date", DateType(), True)
])

# Sample data
data = [
    (1, 3, 5, "2019-08-01"),
    (1, 3, 6, "2019-08-02"),
    (2, 7, 7, "2019-08-01"),
    (2, 7, 6, "2019-08-02"),
    (4, 7, 1, "2019-07-22"),
    (3, 4, 4, "2019-07-21"),
    (3, 4, 4, "2019-07-21")
]

# Create DataFrame
df = spark.createDataFrame(data, schema)

print("Original DataFrame:")
df.show()

print("DataFrame Schema:")
df.printSchema()

# Find authors who viewed their own articles
# Condition: author_id == viewer_id
result_df = df.filter(col("author_id") == col("viewer_id")) \
    .select(col("author_id").alias("id")) \
    .distinct()

print("Authors who viewed their own articles:")
result_df.show()


# Using Join
a = df.alias('a')
b = df.alias('b')
author_viewer_df = a.join(b, ((col('a.author_id') == col('b.author_id')) & (col('a.viewer_id')==col('b.viewer_id'))),
                          how = 'inner'
)
author_viewer_df.select('a.author_id').distinct().orderBy('a.author_id').show()


# Alternative solution using SQL
df.createOrReplaceTempView("article_views")

sql_result = spark.sql("""
    SELECT DISTINCT author_id as id
    FROM article_views
    WHERE author_id = viewer_id
""")

print("SQL Solution:")
sql_result.show()

# Stop SparkSession
spark.stop()


