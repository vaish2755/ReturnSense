import pandas as pd

from hindsight.store import store_return
from hindsight.memory import close_client


df = pd.read_csv("data/returns_sustainability_dataset.csv")

# Keep only actual returned orders
returned = df[df["Return_Status"] == "Returned"].copy()

print(f"Total returned orders: {len(returned)}")
print("Starting ingestion...")


try:
    for count, (_, row) in enumerate(returned.iterrows(), start=1):

        return_data = {
            "order_id": row["Order_ID"],
            "customer_id": row["User_ID"],
            "product_id": row["Product_ID"],
            "category": row["Product_Category"],
            "order_date": row["Order_Date"],
            "return_reason": row["Return_Reason"],
            "days_to_return": row["Days_to_Return"],
            "order_value": row["Order_Value"],
            "return_cost": row["Return_Cost"],
            "profit_loss": row["Profit_Loss"],
            "co2_emissions": row["CO2_Emissions"],
            "packaging_waste": row["Packaging_Waste"],
        }

        store_return(return_data)

        if count % 100 == 0:
            print(f"Processed {count} / {len(returned)} records...")


    print("\nAll 1,450 return records stored successfully!")

finally:
    close_client()