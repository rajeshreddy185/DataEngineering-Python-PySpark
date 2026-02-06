1. Performance: Caching & Persist
Spark is lazy; it recomputes everything from the source unless you tell it to save progress.

cache(): Stores data in memory (shortcut for persist(MEMORY_AND_DISK)).
persist(level): Allows you to choose (Disk only, Memory only, or Off-heap).

```python
df_heavy = df.join(df2).groupBy("id").agg(F.sum("amount"))

# Tell Spark: "Don't re-calculate this join every time I use df_heavy"
df_heavy.cache() 

df_heavy.count() # Trigger 1: Data is now stored in memory
df_heavy.filter(F.col("sum") > 100).show() # Fast: Uses the cache
```

2. The Optimizer: Broadcasting & Explain
Broadcasting: If joining a huge table (1TB) with a tiny one (10MB), Spark usually "shuffles" both.
Broadcasting sends the tiny table to every worker so the big one stays put.
```python
# Forces a BroadcastHashJoin instead of a SortMergeJoin (Shuffle)
df_big.join(broadcast(df_small), "id")

```
explain(): Shows the "Logical and Physical Plan"—it's the X-ray of your query.

3. Structural: Complex Data Types & Explode

Data isn't always flat. You often deal with Arrays (lists) and Maps (key-value).

explode: Takes an array of 3 items and turns that 1 row into 3 rows.

```python
# df has a column 'tags' which is ["tech", "sale"]
# Result: 2 rows, one with "tech", one with "sale"
df.select("product_id", F.explode("tags").alias("single_tag"))
```

4. Custom Logic: UDFs (User Defined Functions)
When Spark's built-in functions fail, you write Python.

Warning: Standard UDFs are slow. Pandas UDFs are fast because they use Arrow to process data in batches.

```python

@F.pandas_udf("string")
def to_upper_case(s: pd.Series) -> pd.Series:
    return s.str.upper()

df.withColumn("name_upper", to_upper_case("name"))

```


5. Partitions: Repartition vs. Coalesce

In PySpark, partitions are the chunks of data distributed across your cluster.
Managing them correctly is the difference between a job that finishes in minutes and one that hangs forever.
While both repartition and coalesce change the number of partitions, 
they do so using very different physical mechanisms.

**repartition(n)**: Increases or decreases partitions. Causes a Shuffle.
**Mechanism**: It performs a Full Shuffle. This means data is physically moved across the network from every worker 
to every other worker to ensure the new partitions are roughly equal in size.
Use Case: * Increasing Parallelism: If you have 100 CPUs but only 10 partitions, 90 CPUs are doing nothing. 
You repartition to 100 to use your full power.
Balancing Data: If your data is "skewed" (some partitions are 1GB and others are 1KB), repartitioning redistributes it evenly.
Cost: Very High. Moving data over a network is the slowest thing in Spark.

```python
df_balanced = df.repartition(200)
```
**coalesce(n):** Only decreases. No Shuffle. (Best before saving to avoid 1,000 tiny files).
**Mechanism**: It is Shuffle-free. Instead of moving data across the whole network, 
it simply "merges" existing partitions on the same or nearby workers. 
It does not try to make the new partitions perfectly equal in size.
Use Case: * Saving Files: If you filter a 1TB dataset down to 1MB, you might still have 1,000 partitions. 
If you save now, you’ll get 1,000 tiny files. Using coalesce(1) before writing merges them into one 
single file efficiently.
Cost: Very Low. Because it avoids the shuffle, it is much faster than repartition.
```python
df.filter(F.col("age") > 90).coalesce(1).write.csv("old_people.csv")
```


6. The "Senior" Problem: Data Skew & Salting
Skew is when 90% of your data belongs to one ID (like "USA"). One worker gets crushed while others sit idle.

Salting: You add a random number to the key (USA_1, USA_2) to split the "mega-key" across workers.

```python

# Add a random "salt" to the join key
df_skewed = df.withColumn("salt", (F.rand() * 10).cast("int"))
df_skewed = df_skewed.withColumn("join_key", F.concat(F.col("id"), F.lit("_"), F.col("salt")))

```


7. Functional Programming: transform, filter, exists
These allow you to manipulate arrays inside a cell without exploding them.

```python

# Square every number in an array column
df.withColumn("squared", F.transform("my_array", lambda x: x * x))

# Keep only numbers > 10 in the array
df.withColumn("high_nums", F.filter("my_array", lambda x: x > 10))
```

8. Storage: Sinks, Sources & Bucketing
Sinks/Sources: Reading and writing (parquet, delta, avro).

Bucketing: Pre-shuffles data on disk. If you always join two tables by user_id, you "bucket" them by user_id. Spark will never need to shuffle them again.


```python
# Write as buckets
df.write.format("parquet") \
    .bucketBy(100, "user_id") \
    .saveAsTable("bucketed_table")
```



