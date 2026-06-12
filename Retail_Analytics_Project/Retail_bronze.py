from pyspark.sql.types import *
from pyspark.sql import SparkSession

#Inferschema >> This Schmea automatically create by pyspark.
#Explicit Schema  >> This Schema is desgined by Developer where developer defines column names and datatypes.

##Explicit Schema >> 

bronze_schema = StructType([
    StructField("transaction_id", IntegerType(), True),
    StructField("order_date", DateType(), True),
    StructField("ship_date", DateType(), True),
    StructField("customer_id", StringType(), True),
    StructField("customer_age", IntegerType(), True),
    StructField("gender", StringType(), True),
    StructField("product_id", StringType(), True),
    StructField("category", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("discount_pct", DoubleType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("payment_type", StringType(), True),
    StructField("order_status", StringType(), True),
    StructField("created_date", DateType(), True)])

spark = (
    SparkSession.builder
    .appName("Retail_Project")
    .master("local[*]")
    .getOrCreate())


input_path = r"C:\Users\LAVI TARAR\OneDrive\ドキュメント\Desktop\Project\Retail_Analytics_Project-Pyspark\retail_sales_raw.csv"
bronze_df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(input_path)
)

#.topandas() >> This is used for convert spark dataframe to pandas dataframe.
pandas_df = bronze_df.toPandas()

# Export to CSV
pandas_df.to_csv(
    r"C:\Users\LAVI TARAR\OneDrive\ドキュメント\Desktop\Project\Retail_Analytics_Project-Pyspark\retail_bronze.csv",
    index=False)

print("CSV file exported successfully")

