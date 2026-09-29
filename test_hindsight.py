from hindsight.outcome import store_outcome
from hindsight.memory import close_client


outcome = {
    "customer_id": "C102",
    "product_id": "S600",
    "recommended_action": "Provide clearer size and measurement guidance",
    "action_taken": "Updated the product size information",
    "outcome": "Customer kept the product",
    "details": "The customer did not return the product after the size information was updated."
}


try:
    store_outcome(outcome)

    print("Outcome stored successfully!")

finally:
    close_client()