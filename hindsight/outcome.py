from .memory import client, BANK_ID


def store_outcome(outcome_data):
    content = f"""
    Outcome for Customer ID: {outcome_data['customer_id']}
    Product SKU: {outcome_data['product_id']}
    Recommended Action: {outcome_data['recommended_action']}
    Action Taken: {outcome_data['action_taken']}
    Outcome: {outcome_data['outcome']}
    Details: {outcome_data['details']}
    """

    client.retain(
        bank_id=BANK_ID,
        content=content
    )

    return True