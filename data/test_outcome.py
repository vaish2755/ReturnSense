import pandas as pd

from hindsight.outcome import store_outcome
from hindsight.memory import close_client


df = pd.read_csv("data/returns_sustainability_dataset.csv")

row = df[df["Return_Status"] == "Returned"].iloc[0]

outcome_data = {
    "order_id": row["Order_ID"],
    "customer_id": row["User_ID"],
    "product_id": row["Product_ID"],
    "recommended_action": "Improve toy size and dimension information",
    "action_taken": "Added clearer product dimensions and size guidance",
    "outcome": "Simulated positive outcome",
    "details": "Demo outcome stored to test whether ReturnSense can remember actions taken after an agent recommendation."
}

print("\n========================================")
print("       STORING RETURN OUTCOME")
print("========================================")

print(f"Order ID: {outcome_data['order_id']}")
print(f"Customer ID: {outcome_data['customer_id']}")
print(f"Product ID: {outcome_data['product_id']}")
print(f"Action: {outcome_data['action_taken']}")

try:
    store_outcome(outcome_data)

    print("\nOutcome stored successfully in Hindsight!")

finally:
    close_client()