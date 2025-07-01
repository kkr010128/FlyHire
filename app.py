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
def table():
    df = pd.read_csv("/Users/kim-youngho/git/FlyHire/data/2506.csv")# 경로를 못찾아서 절대경로로 바꿈
    table_html = df.to_html(classes="table table-striped", index=False)
    return render_template("index.html", table=table_html)





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1241, debug=True)
