import os

from dotenv import load_dotenv
from groq import Groq

from hindsight.recall import recall_for_return
from hindsight.memory import close_client
from agent.prompts import AGENT_SYSTEM_PROMPT


load_dotenv()

groq_client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


def analyze_return(return_data):
    """
    Analyze a new return using:
    1. Hindsight return memories
    2. Hindsight outcome memories
    3. Groq LLM reasoning
    """

    recalled = recall_for_return(return_data)

    return_memories = recalled["return_memories"]
    outcome_memories = recalled["outcome_memories"]

    if return_memories:
        return_text = "\n\n".join(
            f"Return Memory {i + 1}:\n{memory.text}"
            for i, memory in enumerate(return_memories)
        )
    else:
        return_text = "No relevant past return memories were found."

    if outcome_memories:
        outcome_text = "\n\n".join(
            f"Outcome Memory {i + 1}:\n{memory.text}"
            for i, memory in enumerate(outcome_memories)
        )
    else:
        outcome_text = "No relevant previous outcome memories were found."

    user_prompt = f"""
NEW RETURN

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

PAST RETURN EXPERIENCES FROM HINDSIGHT

{return_text}

PREVIOUS RETURNSENSE OUTCOMES FROM HINDSIGHT

{outcome_text}

IMPORTANT:

Use ONLY the PAST RETURN EXPERIENCES section when counting:
- customer returns
- product returns
- unique return Order IDs
- category return patterns

Do NOT count anything from the OUTCOMES section as a return.

Outcome memories can only be used as supporting context about:
- previous recommendations
- actions taken
- previous outcomes
- what ReturnSense learned

Multiple memories with the same Order ID represent ONE return.

Analyze the new return using the relevant Hindsight memories.
Identify meaningful patterns and provide a practical recommendation.
"""

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": AGENT_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv(
        "data/returns_sustainability_dataset.csv"
    )

    row = df[
        df["Return_Status"] == "Returned"
    ].iloc[0]

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

    try:
        print("\n========================================")
        print("        RETURNSENSE AI AGENT")
        print("========================================")

        print("\nNEW RETURN")
        print(f"Customer: {return_data['customer_id']}")
        print(f"Product: {return_data['product_id']}")
        print(f"Category: {return_data['category']}")
        print(f"Reason: {return_data['return_reason']}")

        print("\nAnalyzing Hindsight memories...")

        result = analyze_return(return_data)

        print("\n========================================")
        print("            AGENT RESULT")
        print("========================================")

        print(result)

    finally:
        close_client()