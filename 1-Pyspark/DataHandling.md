1. Pivot (Reshaping Data)
Pivoting turns row values into separate columns. It is an aggregation, so it must be used with groupBy.
To understand Pivot, it helps to see the data transformation from a "Long" format 
(tall and thin) to a "Wide" format (short and fat).



| product | year | amount |
|---------|------|--------|
| iPhone  | 2023 | 1000   |
| iPhone  | 2024 | 1200   |
| MacBook | 2023 | 2000   |
| MacBook | 2024 | 2500   |


```python

# 1. Group by the row identifier (Product)
# 2. Pivot the column you want to turn into headers (Year)
# 3. Aggregate the values (Amount)
pivoted_df = df_sales.groupBy("product") \
                     .pivot("year") \
                     .sum("amount")

pivoted_df.show()
```

| product     | 2023 | 2024 |
|-------------|------|------|
| iPhone     | 1000 | 1200 |
| MacBook     | 2023 | 2500 |




Note: 
If you don't provide a list of values to .pivot(), 
Spark has to scan your entire dataset first just to find the unique values (e.g., finding all years). 
To make it much faster, provide the list explicitly:

```python
# Much faster on large datasets
years = [2023, 2024]
df.groupBy("product").pivot("year", years).sum("amount")

```


2. JSON Extraction

When data arrives as a JSON string in a single column, you can extract fields without parsing the whole thing manually
using get_json_object or from_json.

```python
df.withColumn("user_name", F.get_json_object(F.col("json_col"), "$.user.info.name"))

# Extracting a list from JSON
df.withColumn("tags", F.get_json_object(F.col("json_col"), "$.tags[0]"))
```

When you have a column where every row is a JSON string (common in Kafka streams or NoSQL exports), 
from_json is the most powerful tool because it turns that string into a real Spark Struct (Object).
This allows you to use dot notation (like df.col.field) rather than parsing the string over and over.

Imagine your DataFrame has a column called raw_data that looks like this: {"user_id": 101, "attributes": {"color": "red", "size": "M"}, "tags": ["promo", "web"]}

Step 1: Define the Schema
You define the structure using StructType.

```python

from pyspark.sql.types import StructType, StructField, StringType, IntegerType, ArrayType
from pyspark.sql import functions as F

# Match the JSON structure exactly
schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("attributes", StructType([
        StructField("color", StringType()),
        StructField("size", StringType())
    ])),
    StructField("tags", ArrayType(StringType()))
])
```

Step 2: Apply from_json


```python
# Convert the string column to a Struct column
df_structured = df.withColumn("parsed", F.from_json(F.col("raw_data"), schema))

# Now you can access nested fields easily!
df_final = df_structured.select(
    "parsed.user_id",
    "parsed.attributes.color",
    F.col("parsed.tags")[0].alias("primary_tag")
)

df_final.show()
```



| Feature | get_json_object | from_json |
|---------|-----------------|-----------|
| Effort | Extract one field at a time. | Extract the whole object at once. |
| Performance | Slow for multiple fields (parses string for each field). | Fast (parses the string exactly once). |
| Types | Everything comes out as a String. | Fields keep their types (Integer, Boolean, etc.). |
| Complexity | Good for simple, flat JSON. | Best for deeply nested structures and arrays. |


3. Timestamp vs. Date

Understanding the difference is key for time-series analysis.
| Function                | Output              | Example         | Use Case       |
|-------------------------|---------------------|-----------------|----------------|
| current_date()           | 2026-02-06          | Daily           | partitions      |
| current_timestamp()      | 2026-02-06 16:15:00 | High-precision  | logs           |
| to_date()                | Truncates time      | Removing time   | from a timestamp |
| date_format()            | "Friday, Feb"       | Custom string   | reporting.     |



4. Datetime Math

```python
# Adding/Subtracting time
df.withColumn("next_month", F.add_months(F.col("date"), 1))
df.withColumn("three_days_ago", F.date_sub(F.col("date"), 3))

# Extracting parts
df.select(
    F.year("timestamp"), 
    F.month("timestamp"), 
    F.dayofweek("timestamp") # 1 = Sunday, 7 = Saturday
)
```

5. Default Values (Handling Nulls)

fillna(): Best for "Global" replacements in specific columns.

```python
# Replace nulls in 'category' with 'Unknown'
df_filled = df.fillna({"category": "Unknown", "price": 0})
```