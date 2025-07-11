import json # 사용안함
import flask # 사용안함??
import requests # 사용안함
from requests.exceptions import RequestException
from bs4 import BeautifulSoup # 크롤링할거면 셀레니움이 편할거같음
import pandas as pd
import time,math # 사용안함
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

# 조건 검색 기능 임포트
from filters.filters import filter_employee_count, filter_location


load_dotenv()
apiKey = os.getenv("API_KEY_D")
baseUrl = os.getenv("BASE_URL")
data56 = os.getenv("DATA250623")
data55 = os.getenv("DATA250522")

endPoint = data56
url = f"{baseUrl}{endPoint}"

headers = {"Authorization": f"Infuser {apiKey}"}

app = Flask(__name__)

df = pd.read_csv("data/2506.csv")
tech_stacks_df = pd.read_csv("data/job_tech_stacks.csv")

# GET이면 원본 데이터 그대로 보여준다.
# POST면 form이면 직원 수, 시 값을 받아서 필터 함수 실행한다.
@app.route("/", methods=["GET", "POST"])
def table():
    filtered_df = df.copy() # 시작할 때 원본 데이터프레임 df를 복사한다. 필터링은 복사본에만 적용함. 안정성때문에 해봄.
    selected_employee = None # 직원 수 선택값 초기화
    selected_sido = [] # 시/도 선택값 초기화

    if request.method == "POST":
        # POST 데이터에서 직원 수 값 가져옴
        selected_employee = request.form.get("employeeCount")
        # POST 데이터에서 다중 선택 가능한 값 리스트로 가져온다
        # 다중 요청이기 때문에 무조건 리스트로 받아야함 [서울, 부산, ... ]
        selected_sido = request.form.getlist("sido")
        if selected_employee:
            filtered_df = filter_employee_count(filtered_df, selected_employee)

        if selected_sido:
            filtered_df = filter_location(filtered_df, selected_sido)

    # 필터링된 데이터프레임을 HTML table로 변환
    table_html = filtered_df.to_html(classes="table table-striped", index=False)
    return render_template(
        "index.html",
        table=table_html,
        selected_employee=selected_employee,
        selected_sido=selected_sido
    )

@app.route("/tech_stacks")
def tech_stacks_table():
    image_folder = os.path.join(app.static_folder, 'images')
    images = os.listdir(image_folder)
    images = [img for img in images if img.endswith('.png')]

    # 이미지 파일명에서 직무명 추출 (파일명 형식: 직무_기술스택_그래프.png)
    jobs_in_images = list(set(img.split('_')[0] for img in images))

    return render_template('tech_stacks.html', jobs=jobs_in_images, images=images)

@app.route("/company_tech_stacks/")
def company_tech_stacks():
    return render_template('company_tech_stacks.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1241, debug=True)
