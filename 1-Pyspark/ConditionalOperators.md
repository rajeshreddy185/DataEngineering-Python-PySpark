1. CASE WHEN (when().otherwise())

PySpark does not use the CASE WHEN ... END syntax directly. 
Instead, it chains .when() methods together, finishing with an .otherwise() (which acts as the ELSE).

```python
# SQL Equivalent:
# CASE 
#   WHEN age < 18 THEN 'Child'
#   WHEN age < 65 THEN 'Adult'
#   ELSE 'Senior' 
# END

df.withColumn("age_group", 
    F.when(F.col("age") < 18, "Child")
     .when(F.col("age") < 65, "Adult")
     .otherwise("Senior")
)
```

2. COALESCE (coalesce())
   Just like in SQL, coalesce returns the first non-null value from a list of columns. This is perfect for filling in 
   gaps where data might exist in one column but not another.

```python
# It checks home_phone first; if null, checks cell_phone, etc.

df.withColumn("primary_contact", 
    F.coalesce(F.col("home_phone"), F.col("cell_phone"), F.col("work_phone"))
)
```

3. NULLIF (nullif() - Requires Spark 3.4+)
   In older versions of Spark, you had to simulate NULLIF using when. 
   In newer versions, there is a dedicated function. It returns null if the two arguments are equal; 
   otherwise, it returns the first argument.

```python
Syntax: 
F.when(col1 == col2, None).otherwise(col1) (Old Way) 
or 
expr("nullif(col1, col2)")
```

