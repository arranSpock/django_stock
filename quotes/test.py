import requests
import json
response = requests.get("https://api.twelvedata.com/time_series?apikey=607abcaf08e0464499cea69cbd004534&interval=1day&symbol=AXON&start_date=2024-07-01 21:13:00&format=JSON&end_date=2025-06-30 21:15:00")
api = json.loads(response.content)

try:
    api = json.loads(response.content)
except Exception as e:
    api = 'Error loading...'

print(api)