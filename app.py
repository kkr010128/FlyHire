import json
import flask
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import pandas as pd
import time
import math
import os
from dotenv import load_dotenv
from flask import Flask, render_template


load_dotenv()
apiKey = os.getenv("API_KEY_D")
baseUrl = os.getenv("BASE_URL")
data56 = os.getenv("DATA250623")
data55 = os.getenv("DATA250522")

endPoint = data56
url = f"{baseUrl}{endPoint}"

headers = {"Authorization": f"Infuser {apiKey}"}

app = Flask(__name__)


@app.route("/")
def index():
    try:
        response = requests.get(url, headers=headers)
        try:
            result_json = response.json()
            result_text = json.dumps(result_json, indent=2, ensure_ascii=False)
        except ValueError:
            result_text = response.text
    except RequestException as e:
        result_text = f"Error: {str(e)}"
    return render_template("index.html", result=result_text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1241, debug=True)
