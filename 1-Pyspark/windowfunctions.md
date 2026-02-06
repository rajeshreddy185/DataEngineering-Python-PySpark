**Window Functions**

In PySpark, Window Functions allow you to perform calculations across a "window" of rows that are related to the 
current row. Unlike a groupBy which collapses your data into a single row per group, Window functions keep every 
row intact while adding a calculated value (like a rank or a running total) next to them.

1. The Structure of a Window
To use window functions, you must define a WindowSpec. It has three main parts:

partitionBy: Groups the data (e.g., "Calculate this per customer").
orderBy: Defines the sequence (e.g., "Sort by date").
rowsBetween / rangeBetween: Defines the "frame" (e.g., "Look at the previous 3 rows").


```python
# Define the Window: Partition by Dept, Order by Salary
window_spec = Window.partitionBy("department").orderBy(F.desc("salary"))
```

2. Ranking Functions
Ranking functions are used to assign a number to rows within their group based on the order.

Function          Behavior
------------------ --------------------------------------------------------
row_number()       Unique sequential number (1, 2, 3, 4).
rank()             Leaves gaps after ties (1, 2, 2, 4).
dense_rank()       No gaps after ties (1, 2, 2, 3).
percent_rank()     Relative rank (0.0 to 1.0).

**Get the Top 1 Highest Paid Employee per Department**

```python
df.withColumn("rank", F.row_number().over(window_spec)) \
  .filter(F.col("rank") == 1) \
  .show()
```


NOTE: 

If you call Window.orderBy("date") without a partitionBy, Spark is forced to move all your data to a single computer 
(one executor) to sort it globally. This will likely cause an Out Of Memory (OOM) error on large datasets.