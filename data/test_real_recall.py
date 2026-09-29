import pandas as pd

from hindsight.recall import recall_for_return
from hindsight.memory import close_client


# Load the real dataset
df = pd.read_csv("data/returns_sustainability_dataset.csv")

# Pick one real returned order
row = df[df["Return_Status"] == "Returned"].iloc[0]

# Convert the dataset row into our standard return format
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


print("\n--- NEW RETURN ---")
print(f"Order ID: {return_data['order_id']}")
print(f"Customer ID: {return_data['customer_id']}")
print(f"Product ID: {return_data['product_id']}")
print(f"Category: {return_data['category']}")
print(f"Return Reason: {return_data['return_reason']}")


try:
    memories = recall_for_return(return_data)

    print("\n--- RELEVANT PAST MEMORIES ---")

    if not memories:
        print("No relevant memories found.")

    else:
        for i, memory in enumerate(memories, start=1):
            print(f"\nMemory {i}:")
            print(memory.text)

finally:
    close_client()