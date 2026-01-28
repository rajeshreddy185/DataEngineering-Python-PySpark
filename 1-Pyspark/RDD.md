# Resilient Distributed Datasets (RDDs)

## Core Concept
RDD (Resilient Distributed Dataset) is the fundamental data structure of Apache Spark, designed for distributed computing with fault tolerance.

## Key Characteristics

### 1. Resilient
- **Fault-tolerant** through lineage
- Automatically recovers lost data
- Recomputes missing partitions on failure

### 2. Distributed
- Data is partitioned across cluster nodes
- Enables parallel processing
- Handles large-scale datasets efficiently

### 3. Immutable
- Read-only collection of records
- Operations create new RDDs
- Thread-safe by design

## RDD Operations

### Transformations (Lazy Evaluation)
| Operation | Description | Example |
|-----------|-------------|---------|
| `map()` | Apply function to each element | `rdd.map(lambda x: x*2)` |
| `filter()` | Keep elements that pass condition | `rdd.filter(lambda x: x > 10)` |
| `flatMap()` | Apply function that returns sequence | `rdd.flatMap(lambda x: x.split())` |
| `reduceByKey()` | Aggregate values by key | `rdd.reduceByKey(lambda a,b: a+b)` |

### Actions (Eager Evaluation)
| Operation | Description | Example |
|-----------|-------------|---------|
| `collect()` | Return all elements to driver | `rdd.collect()` |
| `count()` | Count number of elements | `rdd.count()` |
| `first()` | Return first element | `rdd.first()` |
| `take(n)` | Return first n elements | `rdd.take(5)` |
| `saveAsTextFile()` | Save to text files | `rdd.saveAsTextFile("output")` |

## RDD vs DataFrame Comparison

| Feature | RDD (Resilient Distributed Dataset) | DataFrame |
|---------|-------------------------------------|-----------|
| **Structure** | Unstructured. It just sees a collection of objects (Java/Python objects). | Structured. It has a schema (columns and types), like a table in a database. |
| **Optimization** | Manual. Spark doesn't know what's inside, so it can't optimize your code. | Automatic. Uses the Catalyst Optimizer to find the fastest way to run your query. |
| **Ease of Use** | Complex. Requires functional programming (lambdas, maps, filters). | Simple. Uses SQL-like syntax or DSL (e.g., `df.select("name")`). |
| **Data Type** | Type-safe. (In Java/Scala) You know exactly what objects you're handling. | Untyped. (In Python/Scala) Errors often show up at runtime rather than compile time. |
| **Performance** | Slower for structured data due to Java/Python object overhead. | Faster due to optimized in-memory format (Tungsten) and query optimization. |
| **Use Case** | Low-level operations, custom algorithms, unstructured data. | Structured data processing, SQL-like operations, ML pipelines. |

## RDD Creation

### From Collections
```python
data = [1, 2, 3, 4, 5]
rdd = spark.sparkContext.parallelize(data)
```*

