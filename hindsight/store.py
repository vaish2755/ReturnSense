import time

from hindsight_client import Hindsight
from .memory import client, BANK_ID


def store_return(return_data, max_retries=5):
    content = f"""
    Return Experience

    Order ID: {return_data['order_id']}
    Customer ID: {return_data['customer_id']}
    Product ID: {return_data['product_id']}
    Product Category: {return_data['category']}
    Order Date: {return_data['order_date']}

    Return Reason: {return_data['return_reason']}
    Days to Return: {return_data['days_to_return']}

    Order Value: {return_data['order_value']}
    Return Cost: {return_data['return_cost']}
    Profit/Loss: {return_data['profit_loss']}

    CO2 Emissions: {return_data['co2_emissions']}
    Packaging Waste: {return_data['packaging_waste']}
    """

    for attempt in range(1, max_retries + 1):
        try:
            client.retain(
                bank_id=BANK_ID,
                content=content
            )

            return True

        except Exception as error:
            if attempt == max_retries:
                raise error

            wait_time = attempt * 2

            print(
                f"Temporary Hindsight error. "
                f"Retrying in {wait_time}s "
                f"(attempt {attempt}/{max_retries})..."
            )

            time.sleep(wait_time)