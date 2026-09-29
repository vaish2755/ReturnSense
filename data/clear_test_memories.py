import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["HINDSIGHT_API_KEY"]

url = "https://api.hindsight.vectorize.io/v1/default/banks/returnsense/memories"

response = requests.delete(
    url,
    headers={
        "Authorization": f"Bearer {api_key}"
    }
)

print(response.status_code)
print(response.json())