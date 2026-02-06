In PySpark, lead, lag, and rowsBetween are the tools used for Time-Series analysis and Row-Relative calculations. 
They allow you to look backward, forward, or at a specific "slice" of data relative to the current row.


1. Lead and Lag (Looking Back and Forward)
These functions allow you to compare the current row with a previous or subsequent row without performing 
a self-join.

lag(col, offset): Looks back n rows.
lead(col, offset): Looks forward n rows

```python
windowSpec = Window.partitionBy("product_id").orderBy("date")

df.withColumn("yesterday_price", F.lag("price", 1).over(windowSpec)) \
  .withColumn("tomorrow_price", F.lead("price", 1).over(windowSpec)) \
  .withColumn("price_diff", F.col("price") - F.col("yesterday_price"))

```

2. rowsBetween (Defining the "Frame")
While lag and lead look at a single specific row, rowsBetween defines a range (frame) of rows to include in an aggregate
calculation (like a sum or average).
Syntax: .rowsBetween(start, end)

0 is the Current Row.
-1 is the Previous Row.
1 is the Next Row.
Window.unboundedPreceding = The very start of the partition.
Window.unboundedFollowing = The very end of the partition.


```python
# Frame: From start of partition to the current row
running_total = Window.partitionBy("user_id") \
                      .orderBy("date") \
                      .rowsBetween(Window.unboundedPreceding, Window.currentRow)

df.withColumn("total_spent", F.sum("amount").over(running_total))
```

```python
# Frame: 2 rows back + current row (total 3 rows)
moving_avg = Window.partitionBy("sensor_id") \
                   .orderBy("timestamp") \
                   .rowsBetween(-2, Window.currentRow)

df.withColumn("smooth_reading", F.avg("reading").over(moving_avg))
```


```python
# Frame: Entire partition from start to finish
entire_group = Window.partitionBy("category") \
                     .rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

df.withColumn("category_total", F.sum("sales").over(entire_group)) \
  .withColumn("pct_of_total", F.col("sales") / F.col("category_total"))
```
3. The Logic of rangeBetween
When using rangeBetween(start, end), Spark calculates the range based on the value in your orderBy column.
Example: 7-Day Running Window If your current row has a date value of 10, a range of (-7, Window.currentRow) 
will include any row where the date is between 3 and 10.

```python
# Note: The orderBy column must be numeric or a timestamp for rangeBetween
# We often convert dates to unix timestamps (seconds) for this
windowSpec = Window.partitionBy("user_id") \
                   .orderBy("timestamp_seconds") \
                   .rangeBetween(-86400, Window.currentRow) # 86400 seconds = 1 day

df.withColumn("last_24h_sum", F.sum("amount").over(windowSpec))
```


Rows vs. Range
rowsBetween: Counts the physical number of rows (e.g., "3 rows back").
rangeBetween: Looks at the values in the orderBy column (e.g., "3 days back" based on the actual date values,
regardless of how many rows exist in those 3 days).