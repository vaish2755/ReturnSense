import pandas as pd

df = pd.read_csv("data/returns_sustainability_dataset.csv")

returned = df[df["Return_Status"] == "Returned"]

print("Total orders:", len(df))
print("Returned orders:", len(returned))
print("Non-returned orders:", len(df) - len(returned))

print("\nReturn reasons:")
print(returned["Return_Reason"].value_counts())