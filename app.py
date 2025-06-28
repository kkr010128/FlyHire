import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import math
import os
from dotenv import load_dotenv


load_dotenv()
apiKey = os.getenv("API_KEY_D")
baseUrl = os.getenv("BASE_URL")
data56 = os.getenv("DATA250623")
data55 = os.getenv("DATA250522")

endPoint = data56
url = f"{baseUrl}{endPoint}"

headers = {"Authorization": f"Infuser {apiKey}"}

response = requests.get(url, headers=headers)
print(response.text)
