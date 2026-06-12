from pyspark.sql.functions import *
from pyspark.sql import SparkSession
print("Library Imported Sucessfully.")

spark=SparkSession.builder.appName("Gold_file").master("local[*]").getOrCreate()
print("SparkSession Created Sucessfully")

silver_input = r"C:\Users\LAVI TARAR\OneDrive\ドキュメント\Desktop\Project\Retail_Analytics_Project-Pyspark\retail_silver.csv"
silver_df = spark.read.csv(silver_input)
silver_df.show(5)
print("File Read Sucessfully")

#Derived Column >> total_amount

silver_df = silver_df.withColumn(
    "total_amount",
    round(
        col("quantity") * col("unit_price") * (1 - (col("discount_pct") / 100)),2))

## Daily sales Metrics >>>>>>>>>>

daily_sales_df = silver_df.groupBy("order_date").agg(
                      round(sum("total_amount"),2).alias("total_revenue"),
                      count("transaction_id").alias("total_orders"),
                      round(avg("total_amount"),2).alias("avg_order_value"))

daily_sales_df.write .mode("overwrite").option("header", "true").csv("/path/to/output/daily_sales")
print("Daily_Sales DataFrame Exported Sucessfully.")

## City Level revenue Metrics >>>>>>

city_revenue_df=silver_df.groupBy("city","state").agg(
                   round(col("total_amount"),2).alias("city_revenue"),
                   count(col("transaction_id").alias("order_count"),
                         round(avg("total_amount"),2).alias("avg_order_value")))

city_revenue_df.write.mode("overwrite").option("header","true").csv("/path/to/output/daily_sales")
print("City_Revenue DataFrame Exported Sucessfully.")