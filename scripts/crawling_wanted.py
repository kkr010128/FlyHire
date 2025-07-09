import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv, time
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib import rc

# 한글 폰트 설정 (Mac 환경에서 한글 깨짐 방지)
rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 부호 깨짐 방지

ID = "ohhunmi24@gmail.com"  # 원티드 로그인용 이메일
PASSWORD = "As589788@@"     # 원티드 로그인용 비밀번호

# 직군 value (개발 직군)
occupation_value = '518'

# 직무 리스트를 저장할 변수 (크롤링 대상)
job_value_list = []

# 기술 스택 리스트 (사용하지 않음, 추후 확장 가능)
teck_stacks = []

# 크롬 드라이버 옵션 설정
options = Options()
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # 알림 차단
    "profile.default_content_setting_values.geolocation": 2,    # 위치 권한 차단
    "profile.default_content_setting_values.media_stream_mic": 2,  # 마이크 차단
    "profile.default_content_setting_values.media_stream_camera": 2,  # 카메라 차단
}
options.add_experimental_option("prefs", prefs)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_argument("--headless")  # 브라우저 창을 띄우지 않고 실행

# 크롬 드라이버 실행 (자동으로 최신 드라이버 설치)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Selenium 명시적 대기 객체 (최대 5초)
wait = WebDriverWait(driver, 5)

# 원티드 개발 직군 필터 페이지 접속
driver.get('https://www.wanted.co.kr/discovery?job=518&subJob=1024&annual=-0#skill-hired')
print("원티드 홈페이지 접속 완료...")

# 로그인 버튼 클릭
try:
    login_button = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR,
    '#__next > main > div.LoginModal_LoginModal__ZK1sd > div.LoginModal_LoginModal_body__XT3H4 > button.Button_Button__root__MS62F.Button_Button__contained__ftxwc.Button_Button__containedPrimary__oQnx2.Button_Button__containedSizeLarge__f0aza.LoginModal_LoginModal_body_login__fO3og'
    )))
    login_button.click()
    print('로그인 버튼 클릭 성공')
except Exception as e:
    print("로그인 버튼을 찾지 못했습니다.")
    print(e)

# 이메일로 로그인 버튼 클릭
try:
    login_to_email_button = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR,
    '#__next > main > section > div > div > div > div.css-1qafqms > form > div.css-1qsnvsb > button.css-vwpg9b'
    )))
    login_to_email_button.click()
    print('이메일로 로그인 버튼 클릭 성공')
except Exception as e:
    print("이메일로 로그인 버튼을 찾지 못했습니다...")
    print(e)

# 이메일 입력
try:
    id_input = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        '#email'
    )))
    id_input.send_keys(ID)
    print("아이디 제출 성공")
except Exception as e:
    print("아이디 입력에 실패했습니다.")
    print(e)

# 비밀번호 입력
try:
    password_input = wait.until(EC.element_to_be_clickable((
    By.CSS_SELECTOR,
    '#__next > main > section > div > div > div.css-1qjqoce > form > div:nth-child(1) > div.css-1dxhdfz > input'
    )))
    password_input.send_keys(PASSWORD)
    print("비밀번호 제출 완료")
except Exception as e:
    print("비밀번호 제출에 실패했습니다.")
    print(e)

# 로그인 최종 제출 버튼 클릭
try:
    submit_login_button = driver.find_element(By.CSS_SELECTOR,'#__next > main > section > div > div > div.css-1qjqoce > form > div:nth-child(1) > button')
    submit_login_button.click()
    print("로그인을 성공했습니다!")
except Exception as e:
    print("로그인에 실패했습니다...")
    print(e)

# 직군(개발) select 요소 찾기
occupation_select_element = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > label:nth-child(1) > div > select'
)))

# 직무 select 요소 찾기
job_select_element = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > label:nth-child(2) > div > select'
)))

# 경력 select 요소 찾기
career_element = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > label:nth-child(3) > div > select'
)))

# 필터 적용 버튼 요소 찾기
apply_button= wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > button'
)))

# Selenium Select 객체로 변환
occupation_select = Select(occupation_select_element)
occupation_select.select_by_value(occupation_value)  # 개발 직군 선택

job_select = Select(job_select_element)
job_select_options = job_select.options  # 직무 옵션 전체 가져오기

career = Select(career_element)
# career.select_by_index(1)  # 신입 선택 (일부 직무는 신입 없음)

# 직무 옵션 텍스트만 리스트로 저장 (맨 앞은 '전체'이므로 제외)
for option in job_select_options[1:]:
    job_value_list.append(option.text)

def run_job_search():
    """
    각 직무별로 신입(0~1년) 필터를 적용하고, 필터 적용 버튼을 클릭합니다.
    실제 크롤링 전 필터 적용 테스트용 함수입니다.
    """
    for job_value in range(len(job_value_list)):        
        try:    
            job_select.select_by_visible_text(job_value_list[job_value])  # 직무 선택
            career.select_by_index(1)  # 신입 선택
            time.sleep(1)  # 페이지 로딩 대기
            apply_button.click()  # 필터 적용
            print(f"{job_value_list[job_value]}직무 선택!")
            time.sleep(1)  # 페이지 로딩 대기
        except Exception as e:
            print(f"{job_value_list[job_value]}에서 오류 발생 :{e}")
            continue

# 함수 실행 (여기서는 실제 크롤링과 무관, 필터 적용 테스트용)
run_job_search() # 여기서 함수 실행하는데 에러가남 하지만 똑같은 코드를 반복문으로 돌리면 에러가 안남 <- 원인 불명..

# 크롤링 결과를 저장할 리스트
result = []

time.sleep(2)  # 페이지 안정화 대기

# 각 직무별로 기술스택 및 비율 크롤링
for job_value in range(len(job_value_list)):
    try:
        job_select.select_by_visible_text(job_value_list[job_value])  # 직무 선택
        career.select_by_index(1)  # 신입 선택
        time.sleep(1)  # 페이지 로딩 대기
        apply_button.click()  # 필터 적용
        print(f"{job_value_list[job_value]} 직무 선택!")
        time.sleep(1)  # 페이지 로딩 대기

        # 기술스택 정보가 있는 요소 대기 및 추출
        tech_stacks_element = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            '#__next > main > section > article.SkillInfo_SkillInfo__YSa5v > div:nth-child(2) > div.BarList_BarList__GvAW3'
        )))

        tech_stacks_text = tech_stacks_element.text.strip()  # 텍스트 추출

        extracted_stacks = []
        if tech_stacks_text:
            lines = tech_stacks_text.split('\n')  # 줄 단위로 분리

            i = 0
            while i < len(lines):
                name = lines[i].strip()  # 기술스택 이름
                percentage = None

                # 다음 줄이 있고, %가 있으면 비율로 처리
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if '%' in next_line:
                        digits = ''.join(filter(str.isdigit, next_line))
                        percentage = int(digits) if digits else None
                        i += 1  # 비율줄까지 같이 소모

                extracted_stacks.append({
                    'name': name,
                    'percentage': percentage
                })

                i += 1

        else:
            extracted_stacks = []

        print(f"[{job_value_list[job_value]}] 추출된 기술스택: {extracted_stacks}")

        # 추출된 기술스택을 결과 리스트에 추가
        if extracted_stacks:
            for stack in extracted_stacks:
                result.append({
                    '직무': job_value_list[job_value],
                    '기술스택': stack['name'],
                    '비율': stack['percentage']
                })
        else:
            result.append({
                '직무': job_value_list[job_value],
                '기술스택': None,
                '비율': None
            })

    except Exception as e:
        print(f"{job_value_list[job_value]}에서 오류 발생 : {e}")
        result.append({
            '직무': job_value_list[job_value],
            '기술스택': None,
            '비율': None
        })
        continue

# 크롤링 결과를 pandas DataFrame으로 변환 후 CSV로 저장
df = pd.DataFrame(result)
df.to_csv('../data/job_tech_stacks.csv', index=False, encoding='utf-8-sig')
print("CSV 저장 완료!")

# 저장된 CSV를 다시 읽어옴 (혹시 모를 인코딩 문제 방지)
df = pd.read_csv('../data/job_tech_stacks.csv')

# 직무별로 기술스택 비율 그래프 생성 및 저장
job_titles = df['직무'].unique()  # 직무 리스트 추출

for job in job_titles:
    df_filtered = df[df['직무'] == job].copy()  # 해당 직무만 필터링
    
    if df_filtered.empty:
        continue  # 데이터 없으면 건너뜀
    
    df_filtered = df_filtered.sort_values(by='비율', ascending=True)  # 비율 오름차순 정렬
    
    plt.figure(figsize=(10, 6))
    plt.barh(df_filtered['기술스택'], df_filtered['비율'], color='skyblue')  # 수평 막대그래프
    plt.xlabel('비율 (%)')
    plt.title(f'{job} 기술스택 비율')
    plt.xlim(0, 100)
    plt.tight_layout()
    
    # 파일명에 사용할 수 없는 문자 치환
    safe_job_name = job.replace('/', '_').replace(',', '_').replace(' ', '_')
    plt.savefig(f'static/images/{safe_job_name}_기술스택_그래프.png', dpi=300)
    plt.close()

    print(f"{job} 그래프 저장 완료!")

print("모든 직무 그래프 저장 완료!")