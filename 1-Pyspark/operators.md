**1. AND / OR (Boolean Logic)**
In PySpark, you cannot use the Python keywords and/or inside DataFrame operations. You must use the bitwise 
operators & (AND) and | (OR).

You must enclose each condition in parentheses (). If you don't, 
Python's order of operations will cause the script to fail.

```python
# SQL: WHERE age > 25 AND dept = 'Sales'
df.filter((F.col("age") > 25) & (F.col("dept") == "Sales"))

# SQL: WHERE status = 'Error' OR attempts > 3
df.filter((F.col("status") == "Error") | (F.col("attempts") > 3))
```

2. LIKE (Pattern Matching)

Used for partial string matching. It accepts SQL wildcards:

%: Matches any number of characters.
_: Matches exactly one character.

```python 
# SQL: WHERE name LIKE 'A%' (Starts with A)
df.filter(F.col("name").like("A%"))

# SQL: WHERE email LIKE '%@gmail.com' (Ends with @gmail.com)
df.filter(F.col("email").like("%@gmail.com"))

# SQL: WHERE sku LIKE 'A_99' (Starts with A, one random char, then 99)
df.filter(F.col("sku").like("A_99"))
```

3. BETWEEN (Ranges)

Spark has a dedicated .between() method. It is inclusive (it includes the start and end numbers).

```python
# SQL: WHERE salary BETWEEN 50000 AND 100000
df.filter(F.col("salary").between(50000, 100000))
```

4. NOT NULL / IS NULL

```python

# SQL: WHERE email IS NOT NULL (Remove rows with missing emails)
df.filter(F.col("email").isNotNull())

# SQL: WHERE phone IS NULL (Find rows missing a phone number)
df.filter(F.col("phone").isNull())
```

5. The "List Check" (IN / NOT IN)

Instead of writing col == "A" OR col == "B", use .isin(). It accepts a Python list.

```python
# SQL: WHERE country IN ('USA', 'Canada', 'Mexico')
countries = ["USA", "Canada", "Mexico"]
df.filter(F.col("country").isin(countries))

# SQL: WHERE country NOT IN ('USA', 'Canada')
# Note: Use the '~' (tilde) to negate the condition
df.filter(~F.col("country").isin(countries))
```

6.  String Specific Operators

While .like() is good, these methods are often more readable and performant for simple text checks.
Operation 
SQL             | Equivalent      | PySpark Syntax
|---------------|-----------------|------------------|
| Starts With   | LIKE 'Abc%'     | `.startswith("Abc")` |
| Ends With     | LIKE '%xyz'     | `.endswith("xyz")` |
| Contains      | LIKE '%mid%'    | `.contains("mid")` |
| Regex Match   | REGEXP          | `.rlike("^[A-Z]{3}")` |


```python
# Find emails from gmail domains
df.filter(F.col("email").endswith("@gmail.com"))

# Find product codes that start with 'PROD'
df.filter(F.col("sku").startswith("PROD"))
```

7. The "Not Equal" Operator

There are two ways to say "Not Equal" in PySpark.

!=: Standard syntax.

~ (Tilde): Inverts a condition (Logical NOT).

```python
# SQL: WHERE status != 'Active'
df.filter(F.col("status") != "Active")

# Inverting a complex condition
# Find rows where it is NOT (Active AND High Priority)
df.filter(~((F.col("status") == "Active") & (F.col("priority") == "High")))
```

8. Null-Safe Equality (<=>)

In standard SQL/PySpark, NULL == NULL is False. If you want to match rows where both sides 
might be null (e.g., in a Join or Filter), use eqNullSafe.

```python
# This returns True if both columns are NULL, or if both are 5.
df.filter(F.col("col_A").eqNullSafe(F.col("col_B")))
```

9.NaN vs. Null Checks
In data science, NaN (Not a Number) is different from NULL (Missing).

isNull() checks for NULL.

isnan() checks for NaN (only for numeric columns like float/double).

```python
# Filter rows where value is specifically NaN (not just null)
df.filter(isnan(F.col("measurement")))

```

