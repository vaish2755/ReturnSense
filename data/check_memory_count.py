import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["HINDSIGHT_API_KEY"]

url = "https://api.hindsight.vectorize.io/v1/default/banks/returnsense/memories/list"

response = requests.get(
    url,
    headers={
        "Authorization": f"Bearer {api_key}"
    },
    params={
        "limit": 1,
        "offset": 0
    }
)

response.raise_for_status()

data = response.json()

print("Hindsight memory count:", data["total"])