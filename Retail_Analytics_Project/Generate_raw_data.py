import time
import random
from datetime import time , datetime , timedelta
import os
import csv

# Base_dir=os.getcwd()    ##used for Getting Current Directory
# output_dir=os.path.join(Base_dir,"data/raw")
output_file  = r"C:\Users\LAVI TARAR\OneDrive\ドキュメント\Desktop\Project\Retail_Analytics_Project-Pyspark\retail_sales_raw.csv"
num_records= 300_00_0

# os.makedirs(output_dir, exist_ok= True)
# file_path = os.path.join(output_dir,output_file)
file_path=output_file
##Reference Data ----------------------->>>>

cities = [
    ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"),
    ("Houston", "TX"), ("Phoenix", "AZ"), ("Philadelphia", "PA"),
    ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"),
    ("San Jose", "CA")
]

categories = {
    'Electronic' : (100,2000),
    'Fashion' : (20,500),
    'Grocery':(1,50),
    'Furniture' : (800,1000),
    'Sports' : (100,300)
}

payment_types = ['Card','UPI','COD','Crypto',None]
genders = ['M','F','Male','Female',None]
order_statuses = ["Delivered", "Cancelled", "Returned"]
start_date= datetime(2024,1,1,)
end_date= datetime(2026,6,1)

##Helper Function ---------------------------------------------------------->>>>

def random_date(start , end):
    delta = end - start
    return start + timedelta(days=random.randint(0,delta.days))

# Data Generation ----------------------------------------------------------->>>>

with open(file_path,mode='w',newline="",encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow([
    "transaction_id", "order_date", "ship_date", "customer_id", "customer_age",
    "gender", "product_id", "product_category", "quantity", "unit_price",
    "discount_pct", "city", "state", "payment_type", "order_status", "ingestion_date" 
    ])

    for i in range(num_records):
        transaction_id = random.randint(1,num_records//2)
        order_date= random_date(start_date,end_date)
        ship_date = order_date + timedelta(days=random.randint(-3,10))

        customer_id = f'CUST{random.randint(1,2000)}'
        customer_age = random.choice([
            random.randint(18,70),
            random.randint(-10,10),
            random.randint(120,200)
        ])

        gender = random.choice(genders)
        category = random.choice(list(categories.keys()))
        price_min , price_max = categories[category]
        unit_price = random.choice([
            round(random.uniform(price_min,price_max),2),
            -random.uniform(1,100),
            None
        ])

        quantity = random.choice([random.randint(1,20),
                                  0, -random.randint(1,5)])
        discount_pct = random.choice([
            round(random.uniform(0,50),2),
            round(random.uniform(60,150),2)
        ])

        city, state = random.choice(cities)

        writer.writerow([transaction_id , order_date.strftime("%Y-%m-%d"),ship_date.strftime("%Y-%m-%d"),
                         customer_id,customer_age,gender,f"PROD{random.randint(1, 50_000)}",
                         category,quantity,unit_price,discount_pct,city,state,random.choice(payment_types),
                         random.choice(order_statuses),datetime.now().strftime("%Y-%m-%d")])

print(f"Generated {num_records} records.")









