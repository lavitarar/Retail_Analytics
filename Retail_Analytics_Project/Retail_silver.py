from pyspark.sql.functions import *
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('silver_file').master("local[*]").getOrCreate()
print("Spark Session Created sucessfully")

input_path = r"C:\Users\LAVI TARAR\OneDrive\ドキュメント\Desktop\Project\Retail_Analytics_Project-Pyspark\retail_bronze.csv"
bronze_df = spark.read.option('header','true').option('inferSchema','true').csv(input_path)

print('Bronze Count:',bronze_df.count())
# bronze_df.printSchema()


# Remove Duplicate >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

bronze_df.groupBy("transaction_id").count().filter(col("count") > 1).show(truncate=False)
silver_df= bronze_df.drop_duplicates(['transaction_id'])
print("After Delete Duplicate :",silver_df.count())


# Date Correction >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

bronze_df.filter(col("ship_date") < col("order_date")).show(5)

silver_df = silver_df.withColumn(
    'ship_date',
    when(col("ship_date") < col("order_date"),None).otherwise(col("ship_date")))

# Quantity and price cleaning >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

silver_df.filter(col('quantity') >=0).show(5)

silver_df.filter(col('quantity') > 0).show(5)

silver_df.filter(col('unit_price') <=0).show(5)

silver_df = silver_df.withColumn(
    "unit_price",
    when((col("unit_price") < 0) | (col("unit_price").isNull()),0).otherwise(col("unit_price"))
)

# Discount Cleaning >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

silver_df.filter(
    (col("discount_pct") < 0) | (col("discount_pct") > 100)).show(5)

silver_df = silver_df.withColumn(
    "discount_pct", 
    when((col("discount_pct") < 0) |(col("discount_pct") > 100),0)
    .otherwise(col("discount_pct"))
)

#Customer Age Cleaning >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

silver_df = silver_df.withColumn(
    "customer_age",
    when((col("customer_age") < 15) | (col("customer_age") > 100), None)
    .otherwise(col("customer_age"))
)

#Standardize Gender >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

silver_df.groupBy("gender").count().show()

silver_df = silver_df.withColumn(
    "gender",
    when(upper(trim(col("gender"))) == "MALE","M")
    .when(upper(trim(col("gender"))) == "FEMALE",'F')
    .when(col("gender").isin("M","F"),col("gender"))
    .otherwise(None)
)

# Standarize Payment System >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

silver_df.filter(
    col("payment_type").isin("Card", "COD", "UPI")).show(5)

silver_df = silver_df.withColumn(
    "payment_type",
    when(
        col("payment_type").isin("Card", "UPI", "COD"),
        col("payment_type"))
        .otherwise(None))

print("Silver Dataframe Stored Successfully.")
print("Silver count >> ",silver_df.count())

## Write Silver Layer >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

silver_final_df = silver_df.toPandas()
silver_output_path = r"C:\Users\LAVI TARAR\OneDrive\ドキュメント\Desktop\Project\Retail_Analytics_Project-Pyspark\retail_silver.csv"

silver_final_df.to_csv( silver_output_path,  index=False)
print("Silver Dataframe Exported Sucessfully.")
print("Total Number of Rows : ",silver_final_df.count())
