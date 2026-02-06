# PySpark DataFrames

## Introduction
A DataFrame is a distributed collection of data organized into named columns, similar to a table in a relational database or a data frame in R/Python (pandas).

## Key Characteristics

### 1. Structured Data Organization
- **Columns**: Named headers that provide structure
- **Rows**: The actual data records
- **Schema**: Metadata defining data types for each column
- **Partitions**: Data is distributed across a cluster but appears as a single table

### 2. Performance Advantages Over RDDs
While RDDs are unstructured "blobs" of data, DataFrames have a defined schema that enables powerful optimizations:

#### A. Catalyst Optimizer (The Query Optimizer)
The Catalyst Optimizer analyzes and optimizes DataFrame operations:

- **Query Optimization**: Rewrites queries for better performance
- **Predicate Pushdown**: Moves filters earlier in the execution plan
- **Constant Folding**: Pre-computes constant expressions
- **Column Pruning**: Only reads necessary columns from storage

*Example*: When joining tables and filtering by year, Catalyst pushes the filter before the join to minimize data processing.

#### B. Project Tungsten (The Performance Engine)
Tungsten provides low-level optimizations:

- **Off-Heap Memory Management**: Reduces garbage collection overhead
- **Cache-aware Computation**: Optimizes for CPU cache efficiency
- **Code Generation**: Generates optimized bytecode at runtime
- **Compact Binary Format**: Reduces memory usage and improves processing speed

## Key Benefits

1. **Schema Awareness**
   - Enables better optimization
   - Provides better error checking
   - Enables more intuitive API

2. **High-level API**
   - SQL-like operations
   - Built-in functions for common transformations
   - Seamless integration with Spark SQL

3. **Performance**
   - Up to 100x faster than RDDs for certain operations
   - Automatic optimization of execution plans
   - Efficient memory usage

#### SELECT

```
select name, age from table;

```

```python
 
df.select("name", "age")
df.select(df.name, df.age)
df.select(F.col("name"), F.col("city"))

```

#### WHERE

```
select * from where age > 21 

```
```python
# Simple string filter
df.filter("age > 21")

# Multiple conditions in a string
df.where("age > 21 AND city = 'New York'")

df.filter(col("age") > 21)
df.where(df.age > 21)

Handling multiple conditions
AND	&	df.filter((col("age") > 21) & (col("status") == "Active"))
OR	|	df.filter((col("city") == "NY") | (col("city") == "SF"))
NOT	~	df.filter(~(col("status") == "Retired"))

Filter by List (isin): df.filter(col("country").isin(["USA", "Canada", "Mexico"]))
Search for Text (contains / startswith): df.filter(col("email").contains("@gmail.com"))
Handle Nulls: df.filter(col("phone_number").isNotNull())

```
#### GROUPby

```
df.groupBy("Department").count().show()
df.groupBy("Department", "City").avg("Salary").show()
df.groupBy("Department").agg(
    F.count("EmployeeID").alias("Employee_Count"),
    F.sum("Salary").alias("Total_Payroll"),
    F.max("Salary").alias("Highest_Salary")
).show()

```

#### GROUP_CONCAT
In PySpark, there isn’t a single function with that name. Instead, we can achieve this by combining two functions
collect_list(): Grabs all values in the group and puts them in a list.
collect_set(): Grabs all unique values in the group and puts them in a list.
concat_ws(): Stands for "concatenate with separator." It turns the list into a single string.

```python
df.groupBy("department").agg(
    F.concat_ws(", ", F.collect_list("employee_name")).alias("all_employees")
).show()

```

#### HAVING

In PySpark's DataFrame API, there is no specific .having() method. 
Instead, we can achieve the same result by simply calling .filter() (or its alias .where()) after your aggregation.
In SQL, HAVING exists because the WHERE clause can't see aggregated values (like sum or count). 
In PySpark, once you run .agg(), the result is just another DataFrame, so you can filter it normally.

```
SELECT dept, COUNT(*) as count 
    FROM sales_data 
    GROUP BY dept 
    HAVING count > 5
```

```python

df.groupBy("dept") \
  .agg(F.sum("sales").alias("total")) \
  .filter(F.col("total") > 1000) \
  .show()

```

In PySpark, orderBy() and sort() are identical.
Sorting in a distributed system is a "wide transformation," meaning Spark has to move data across the network (shuffle)
to ensure that the rows are in the correct order relative to each other across the entire cluster.

```python
# These three lines do the exact same thing
df.orderBy("age").show()
df.sort("age").show()
df.orderBy(df.age.asc()).show()

df.orderBy(F.asc("department"), F.desc("salary")).show()

```

Spark allows us to decide if they should appear at the very beginning or the very end of your results, regardless of 
whether we are sorting ascending or descending.

```python
asc_nulls_first() / asc_nulls_last()
desc_nulls_first() / desc_nulls_last()

df.orderBy(F.asc_nulls_last("name")).show()

```

In PySpark, there are two ways to handle unique values. While distinct() is the direct equivalent of the SQL

distinct()

This is the simplest form. It looks at the entire row. If every single column
in Row A is identical to Row B, one of them is removed.

dropDuplicates()

In the real world, you often have rows that are mostly duplicates (e.g., the same User ID but recorded at different 
timestamps). distinct() won't help here because the timestamps are different.dropDuplicates() allows us to specify 
subset columns to define what counts as a duplicate.

```
1. distinct(): The All-or-Nothing Approach
2. df.dropDuplicates(["email"]).show() or df.dropDuplicates(["first_name", "last_name"]).show()
```

Counting Distinct Values

If we don't want to remove rows but just want to know how many unique values exist, use countDistinct().

```python
df.select(F.countDistinct("customer_id")).show()

```

#### LIMIT

In PySpark, limit() is a transformation used to restrict the number of rows in a DataFrame. While it’s simple to use.

To get the first n rows of a DataFrame as a new DataFrame:

```python
small_df = df.limit(10)

```
The "Top-N" Pattern (Order Matters!)
In a distributed system, data doesn't have a guaranteed "natural" order. If you just call df.limit(10),
you might get different rows every time you run the code.
To get a consistent "Top-N" result, you must always combine limit() with orderBy().

```python
top_earners = df.orderBy(F.desc("salary")).limit(5)
```

limit() always takes the first rows it finds. If you want a random selection, use df.sample() instead.
If you use limit(1000000).collect(), you might crash your Driver program because you're trying 
to shove a million rows into the local RAM of a single machine.

| Method | Type | Result | Use Case |
|--------|------|--------|----------|
| `limit(n)` | Transformation | Returns a new DataFrame | Use when you want to continue processing a smaller subset of data |
| `show(n)` | Action | Prints to the console | Use for a quick visual check. |
| `take(n)` | Action | Returns a Python List of Rows | Use when you want to bring data into local Python memory for processing |

#### Insert Into

There are two main ways to perform an "Insert Into" operation. Unlike a traditional database where we might insert 
one row at a time, Spark is designed for bulk inserts—adding an entire DataFrame to an existing table or storage location at once.
**1. The Direct Way: df.write.insertInto()**

```python
df.write.insertInto("production_table")
```

```
 Column Order Matters! > insertInto matches columns by position, not by name. If your DataFrame has columns (age, name)
 but the table has (name, age), Spark will swap the data into the wrong columns without warning. Always ensure your 
 DataFrame columns are in the exact same order as the target table.
```
**2. The Robust Way: df.write.saveAsTable()**

This is often preferred because it gives you more control using modes.

```
df.write.mode("append").saveAsTable("production_table")
```

Key Differences in Modes:
append: Adds new data to the end of the existing 
table.overwrite: Deletes the old data and replaces it with the new DataFrame 
content.ignore: If the table already exists, Spark does nothing (no error, no data added).
errorIfExists: (Default) Throws an error if the table is already there.


**3. Inserting into a File Path** 

If you aren't using a "table" but are writing directly to S3, HDFS, or a local folder (e.g., Parquet or Delta files), 
you use .save() or the format-specific method:Python# Appending to a folder of Parquet files
```
df.write.mode("append").parquet("/mnt/data/sales_history/")
```



| SQL Command | PySpark Equivalent | Behavior |
|--------------|--------------------|----------|
| INSERT INTO table | df.write.insertInto("table") | Positional. Column order must match exactly. |
| INSERT INTO table | df.write.mode("append").saveAsTable("table") | Named. Matches based on column names (usually). |
| INSERT OVERWRITE | df.write.mode("overwrite").saveAsTable("table") | Replaces entire table content. |

#### UPDATE

DataFrames are immutable. This means you cannot technically "update" a row in place like you would in a SQL database
In Spark is actually a transformation where you create a new DataFrame based on the old one with the changes applied.

1. The Column-Level "Update" (withColumn)

The most common way to update values is by using the .withColumn() method combined with when() and otherwise(). 
This acts like a CASE WHEN statement in SQL.

```
df_updated = df.withColumn("salary", 
    F.when(F.col("department") == "Sales", F.col("salary") * 1.1)
     .otherwise(F.col("salary"))
)
```

2. The "Nuclear" Update: Overwrite
If you need to update a large portion of a table sitting in a folder (like S3 or HDFS), the standard practice is to read 
the data, modify it, and overwrite the existing location.
```
Read -> Modify -> Overwrite
df = spark.read.parquet("/data/sales")
df_new = df.withColumn("status", F.lit("Processed"))

df_new.write.mode("overwrite").parquet("/data/sales")
```

#### SET

Setting values in a Column

```
df = df.withColumn("status", F.lit("Active"))
```
#### DELETE

In PySpark, just like with UPDATE, you have to keep in mind that DataFrames are immutable. You don't actually "delete" 
data from a DataFrame; you create a new DataFrame that simply doesn't include the rows you want to get rid of
.mode("overwrite")	Refreshing an entire table.	Yes, replaces old data.

#### TRUNCATE
In the Spark world, TRUNCATE is used to wipe all the data from a table while keeping the structure (schema) and metadata 
intact. It is the "reset button" for a table.

```python

empty_df = existing_df.limit(0) 
empty_df.write.mode("overwrite").save("/data/sales_records")

```

#### CREATE (from a Schema)

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# 1. Define the schema
schema = StructType([
    StructField("user_id", IntegerType(), True),
    StructField("username", StringType(), True)
])

# 2. Create an empty DataFrame and save as table
spark.createDataFrame([], schema).write.saveAsTable("users_table")
```

#### INDEX

In traditional databases (like MySQL or PostgreSQL), an INDEX is a separate file that acts like the index in the back
of a book, allowing the database to find a specific row without reading the whole table.

In standard Apache Spark/PySpark, there is no such thing as a traditional index. Because Spark is designed to scan 
massive amounts of data in parallel, it uses different strategies to achieve "index-like" performance.

If you are using Delta Lake (the optimized layer on top of Spark), 
you get something very close to a real index called Z-Order Clustering
With Z-Order: Data is clustered. File A has IDs 1-100, File B has 101-200. To find ID = 50,
Spark reads File A and skips everything else.

```python
OPTIMIZE sales_table ZORDER BY (customer_id)
```


#### VIEW

In Spark, a VIEW is a virtual table. It doesn’t actually store data on your disk; instead, 
it stores a query that runs every time you access the view.

1.local temp view

```python
df.createOrReplaceTempView("v_sales_data")
```

2.global view

```python
df.createGlobalTempView("global_sales")
```
3.permanent view

```python
spark.sql("""
    CREATE VIEW IF NOT EXISTS final_report AS
    SELECT name, SUM(salary) FROM employee_table GROUP BY name
""")
```

4.Cache 
If you have a complex View that joins 10 tables and you query it five times in your script, 
Spark might perform those 10 joins five times.If you are going to use a view repeatedly, you should Cache it.
```spark.catalog.cacheTable("v_sales_data")```


#### SCHEMA

While Spark can guess your schema using Schema Inference, defining it manually is considered a best practice for 
production because it's faster, safer, and prevents your job from crashing if a stray "abc" shows up in a numeric column.

A. The Programmatic Way (StructType)
This is the most robust method. You use StructType to represent the row and StructField for each column.
```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

schema = StructType([
    StructField("id", IntegerType(), False),      # Name, Type, Nullable?
    StructField("name", StringType(), True),
    StructField("salary", DoubleType(), True)
])

df = spark.read.schema(schema).csv("employees.csv")
```

B. The DDL String Way (Cleaner Syntax)
If you prefer SQL-style syntax, Spark allows you to define a schema using a simple string. 
This is much easier to read and write.

```
ddl_schema = "id INT, name STRING, salary DOUBLE"
df = spark.read.schema(ddl_schema).csv("employees.csv")
```

| Feature | inferSchema=True | Manual Schema |
|---------|-------------------|----------------|
| Speed | Slow (requires an extra pass over data). | Fast (no data scanning needed). |
| Reliability | Might guess wrong (e.g., ZIP codes as Integers). | You have 100% control. |
| Data Quality | Corrupt rows might slip through. | Corrupt rows can be caught or nulled |


**Viewing and Managing Schemas**

Once a DataFrame is created, you can inspect or manipulate its schema with these commands:

df.printSchema(): Displays a tree-like view of the schema.
df.schema: Returns the StructType object (useful for passing to other DFs).
df.columns: Returns a list of just the column names.
df.dtypes: Returns a list of tuples (column_name, data_type).