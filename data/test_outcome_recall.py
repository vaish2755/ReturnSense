import pandas as pd

from hindsight.recall import recall_memories
from hindsight.memory import close_client


df = pd.read_csv("data/returns_sustainability_dataset.csv")

row = df[df["Return_Status"] == "Returned"].iloc[0]

query = f"""
Find the ReturnSense outcome for this return:

Order ID: {row['Order_ID']}
Customer ID: {row['User_ID']}
Product ID: {row['Product_ID']}

Look for:
- recommended action
- action taken
- outcome
- details
"""

print("\n========================================")
print("       RECALLING STORED OUTCOME")
print("========================================")

try:
    memories = recall_memories(query)

    if not memories:
        print("\nNo outcome memory found.")

    else:
        for i, memory in enumerate(memories, start=1):
            print(f"\nMemory {i}:")
            print(memory.text)

finally:
    close_client()