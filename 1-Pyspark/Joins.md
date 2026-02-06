**JOIN**

In PySpark, a JOIN is used to combine two DataFrames based on a common key. 
Because Spark is a distributed system, joins are often the most "expensive" part of a script because they usually 
require moving large amounts of data across the network (shuffling).

1. Basic Syntax
```python 
The syntax is straightforward: df_left.join(df_right, expression, join_type).
```
1. Inner Join (The Default)
Logic: Keeps only the rows where there is a match in both tables.

```python
# Joining 'employees' and 'departments' on the 'dept_id' column
joined_df = employees.join(departments, employees.dept_id == departments.id, "inner")
df_emp.join(df_dept, "dept_id", "inner").show()

```
2. Left (Outer) Join
Logic: Keeps all rows from the left table. If there’s no match on the right, it fills the right columns with null.

```python
# All employees, including those not assigned to a department
df_emp.join(df_dept, "dept_id", "left").show()
```

3. Right (Outer) Join
Logic: Keeps all rows from the right table. If an employee isn't in a department, the employee columns will be null.
```python
# All departments, even those with no employees
df_emp.join(df_dept, "dept_id", "right").show()
```

4. Full (Outer) Join
Logic: Keeps everything. It matches where it can and fills null everywhere else.
```python
# Combined list of all employees and all departments
df_emp.join(df_dept, "dept_id", "full").show()
```

5. Left Semi Join
Logic: This is like a filter. It returns rows from the left table that have a match on the right, 
but it does not show columns from the right table
```python
# Only show employee names who are in a registered department
# Result: Only columns from df_emp will appear
df_emp.join(df_dept, "dept_id", "left_semi").show()
```

6. Left Anti Join
Logic: The exact opposite of Semi. It returns rows from the left table that do not have a match on the right.
```python
# Find "Ghost" employees (employees assigned to a dept_id that doesn't exist)
df_emp.join(df_dept, "dept_id", "left_anti").show()
```

7. Cross Join
Logic: Every row from the left table is joined with every row from the right (Cartesian Product). 
Caution: This can create massive datasets (Rows_A * Rows_B).
```python
# Every possible combination of employee and department
df_emp.crossJoin(df_dept).show()
```


#### **NOTE**

**Column Name Conflict**
If both DataFrames have a column named dept_id, using the string "dept_id" in the join prevents duplicate columns:

Good: df_emp.join(df_dept, "dept_id", "inner") (Results in one dept_id column)

Bad: df_emp.join(df_dept, df_emp.dept_id == df_dept.dept_id) 
(Results in two dept_id columns, which causes errors in later steps)

**why, how**

It comes down to how Spark’s Catalyst Optimizer handles column references during the joining process.
**Why does it happen?**

When you use the expression df_emp.dept_id == df_dept.dept_id, Spark treats this as a boolean condition. 
It says: "Go find rows where these two separate pointers are equal."

Because you are explicitly referencing two different columns from two different "source" objects, 
Spark keeps both in the resulting DataFrame to be safe. It doesn't want to assume you want to throw one away.

The result? 
A DataFrame with two columns named dept_id. If you then try to run df.select("dept_id"),
Spark panics because it doesn't know which one you want. This is called an Ambiguous Reference Error.

**How does the string method fix it?**

When you pass the join key as a simple string "dept_id", 
you are telling Spark to perform a Using Join (similar to JOIN ... USING(column) in SQL).

Three Ways to Solve the "Bad" Join
If you must use the expression syntax (for example, if you need to join df_emp.id with df_dept.dept_id where the names are different), here is how you handle it:

1. Drop the duplicate column immediately
The most common "quick fix."

```python

df_joined = df_emp.join(df_dept, df_emp.dept_id == df_dept.dept_id).drop(df_dept.dept_id)
```
2. Use Aliasing
Give your DataFrames nicknames so you can tell the columns apart.

```python

from pyspark.sql import functions as F

df_joined = df_emp.alias("emp").join(df_dept.alias("dept"), F.col("emp.dept_id") == F.col("dept.dept_id"))

# Now you can select specifically from one side
df_joined.select("emp.dept_id", "emp_name", "dept_name").show()
```
3. Rename before joining
Clean up your data before the join even happens.

```python

df_dept_renamed = df_dept.withColumnRenamed("dept_id", "d_id")
df_joined = df_emp.join(df_dept_renamed, df_emp.dept_id == df_dept_renamed.d_id)
```