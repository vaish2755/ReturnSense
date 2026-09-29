import pandas as pd

from agent.agent import analyze_return
from hindsight.outcome import store_outcome
from hindsight.memory import close_client


df = pd.read_csv("data/returns_sustainability_dataset.csv")

row = df[df["Return_Status"] == "Returned"].iloc[0]

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


print("\n========================================")
print("       RETURNSENSE FULL PIPELINE")
print("========================================")

print("\nSTEP 1: NEW RETURN")
print(f"Customer: {return_data['customer_id']}")
print(f"Product: {return_data['product_id']}")
print(f"Category: {return_data['category']}")
print(f"Reason: {return_data['return_reason']}")


try:
    print("\nSTEP 2: AI AGENT ANALYSIS")

    result = analyze_return(return_data)

    print("\n--- AGENT RESULT ---")
    print(result)

    print("\nSTEP 3: STORE AGENT OUTCOME")

    outcome_data = {
        "order_id": return_data["order_id"],
        "customer_id": return_data["customer_id"],
        "product_id": return_data["product_id"],
        "recommended_action": result,
        "action_taken": "Simulated action for hackathon demonstration",
        "outcome": "Simulated outcome",
        "details": (
            "The AI agent's recommendation was stored in Hindsight "
            "so future ReturnSense analyses can use this past experience."
        )
    }

    store_outcome(outcome_data)

    print("Outcome stored successfully in Hindsight!")

    print("\n========================================")
    print("       FULL PIPELINE COMPLETED")
    print("========================================")

finally:
    close_client()