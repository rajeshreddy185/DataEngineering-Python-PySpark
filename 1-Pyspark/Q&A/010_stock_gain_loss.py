from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql import SparkSession, functions as F, Window

stock_data = [
    ("Leetcode", "Buy", 1, 1000),
    ("Corona Masks", "Buy", 2, 10),
    ("Leetcode", "Sell", 5, 9000),
    ("Handbags", "Buy", 17, 30000),
    ("Corona Masks", "Sell", 3, 1010),
    ("Corona Masks", "Buy", 4, 1000),
    ("Corona Masks", "Sell", 5, 500),
    ("Corona Masks", "Buy", 6, 1000),
    ("Handbags", "Sell", 29, 7000),
    ("Corona Masks", "Sell", 10, 10000)
]

stock_schema = StructType([
    StructField("stock_name", StringType(), True),
    StructField("operation", StringType(), True),
    StructField("operation_day", IntegerType(), True),
    StructField("price", IntegerType(), True)
])

spark = SparkSession.builder.appName('StockGainLoss').getOrCreate()
stock_df = spark.createDataFrame(stock_data, stock_schema)

stock_df.show()

window_spec = Window.partitionBy(F.col('stock_name'), F.col('operation')).orderBy(F.col('operation_day'))
ranked_df = stock_df.withColumn('rank', F.row_number().over(window_spec))
buy_df = ranked_df.filter(F.col('operation') == 'Buy').withColumn('buy_price', F.col('price'))
sell_df = ranked_df.filter(F.col('operation') == 'Sell').withColumn('sell_price', F.col('price'))

joined_df = buy_df.join(sell_df, on=((buy_df.stock_name==sell_df.stock_name)&(buy_df.rank==sell_df.rank)), how='inner')
joined_df.select(
        buy_df.stock_name,
        (F.col('sell_price')-F.col('buy_price')).alias('gain_loss')
        ).groupBy(F.col('stock_name'), F.col('operation')
        ).agg(F.sum(buy_df.stock_name)).alias('gain_loss').orderBy(buy_df.stock_name).show()

