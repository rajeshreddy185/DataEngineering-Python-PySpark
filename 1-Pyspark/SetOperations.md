**Set Operations**

In PySpark, Set Operations allow you to combine or compare two DataFrames based on their rows. 
Unlike joins, which combine columns from different tables, set operations deal with the vertical alignment 
of data—essentially treating DataFrames like mathematical sets.

To perform these operations, both DataFrames must have the same schema (number of columns and data types).

1. Union

Matches columns by position. If df1 has (name, age) and df2 has (age, name), 
Spark will shove names into the age column!

```python
df_combined = df1.union(df2)
```

2. UnionByName

Matches columns by name. This is much safer for production grade code.

```python
# Safer way to combine data if column orders might differ
df_combined = df1.unionByName(df2)
```

If you have data coming in daily with slightly different schemas (e.g., a new column was added on Tuesday),
you can use allowMissingColumns.

```python
# Combines DataFrames even if one has columns the other doesn't
# Missing columns will be filled with 'null'
df_merged = df_monday.unionByName(df_tuesday, allowMissingColumns=True)
```

3. UnionAll

In traditional SQL, UNION removes duplicates while UNION ALL keeps them. In PySpark:
union() behaves like UNION ALL (it keeps duplicates).
To get a unique set of rows, you must explicitly call .distinct().

```python
df_unique_combined = df1.union(df2).distinct()
```

4. Intersect
These are powerful for data validation and identifying changes between datasets.

```python
# 1. INTERSECT: Find users who appear in both the 'active' and 'premium' tables
both = active_df.intersect(premium_df)
```

5. Except

```python 
# 2. EXCEPT: Find users who are 'active' but NOT 'premium'
# Note: 'subtract' and 'exceptAll' are commonly used
non_premium = active_df.subtract(premium_df)
```
Finding Deleted Records
If you have a snapshot of data from yesterday and today, you can find what was deleted 
by subtracting today from yesterday.

```python
deleted_records = yesterday_df.subtract(today_df)
```

6. exceptAll

In PySpark subtract,exceptAll these are two ways to find the difference between DataFrames.
The difference lies in how they handle duplicates.

Method|Behavior|SQL Equivalent
-----|-------|---------------
subtract()|Returns unique rows in A not in B. (Removes duplicates from the result).|EXCEPT
exceptAll()|Returns all occurrences in A not in B. (Preserves duplicate counts).|EXCEPT ALL

Imagine df1 has the name "Alice" 3 times, and df2 has "Alice" 1 time.
```python 
df1.subtract(df2)
```
will return 0 Alices (it sees "Alice" in both and removes the entire "set").

```python
df1.exceptAll(df2)
``` 
will return 2 Alices (3 - 1 = 2).


###### **2. Why there is not difference between union() and UNION ALL?**

In traditional SQL databases, UNION (which removes duplicates) is the default, 
and UNION ALL (which keeps them) is the "extra" option. In Spark, it’s the opposite.

**The reason is Performance.**

A. The Cost of "Distinct"
   To remove duplicates (as in a traditional UNION), Spark must:
   Compare every single row with every other row.
   Shuffle the data across the network so that identical rows from different computers 
   end up on the same machine to be compared.
   Perform a "Sort" or "Hash" operation.
   This is an expensive and slow operation in a distributed system.

B. The Efficiency of "Union"
   union() in Spark is a narrow transformation. Spark simply takes the pointers to the data in Table A and the pointers 
   to Table B and puts them in a single list. No data is moved across the network. 
   It is essentially "free" in terms of processing time.

**Design Philosophy**: 
          Spark defaults to the fastest possible operation. Since deduplication is slow, 
          Spark makes union() a simple append and requires you 
          to explicitly call .distinct() if you are willing to pay the performance price for uniqueness.
