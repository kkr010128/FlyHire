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
from flask import Flask, render_template, request


load_dotenv()
apiKey = os.getenv("API_KEY_D")
baseUrl = os.getenv("BASE_URL")
data56 = os.getenv("DATA250623")
data55 = os.getenv("DATA250522")

endPoint = data56
url = f"{baseUrl}{endPoint}"

headers = {"Authorization": f"Infuser {apiKey}"}

app = Flask(__name__)

df = pd.read_csv("/Users/kim-youngho/git/FlyHire/data/2506_to_test.csv")# 경로를 못찾아서 절대경로로 바꿈

def filter_employee_count(target):
    if target == "50":
        return df[df['가입자수'] <= 50]
    elif target == "51":
        return df[(df['가입자수'] >= 51) & (df['가입자수'] <= 300)]
    elif target == "301":
        return df[(df['가입자수'] >= 301) & (df['가입자수'] <= 1000)]
    elif target == "1001":
        return df[(df['가입자수'] >= 1001) & (df['가입자수'] <= 10000)]
    elif target == "10001":
        return df[df['가입자수'] >= 10001]
    else:
        return df


@app.route("/", methods=["GET","POST"])
def table():
    if request.method == "POST":
        target = request.form.get("employeeCount")
        filtered = filter_employee_count(target)
        table_html = filtered.to_html(classes="table table-striped", index=False)
    else:
        target = "50"
        table_html = df.to_html(classes="table table-striped", index=False)
    return render_template("index.html", table=table_html, selected=target)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1241, debug=True)
