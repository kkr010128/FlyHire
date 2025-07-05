from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

# 원티드 아이디, 비번
ID = "ohhunmi24@gmail.com"
PASSWORD = "As589788@@"


# 직군 : 개발
occupation_value = '518' # 이거 select list 에서 개발임

# 직무 : 개발 관련된 것들..
job_value_list = []

# 기술 스택
teck_stacks = []


options = Options()
prefs = {
    "profile.default_content_setting_values.notifications": 2,  # 알림 차단
    "profile.default_content_setting_values.geolocation": 2,    # 위치 권한 차단
    "profile.default_content_setting_values.media_stream_mic": 2,  # 마이크 차단
    "profile.default_content_setting_values.media_stream_camera": 2,  # 카메라 차단
}
options.add_experimental_option("prefs", prefs)

# GUI 없이 실행(필요하면 주석 해제)
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
options.add_argument("--headless")

# ✅ 드라이버 실행
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 5)

driver.get('https://www.wanted.co.kr/discovery?job=518&subJob=1024&annual=-0#skill-hired')
print("원티드 홈페이지 접속 완료...")

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

try:
    id_input = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        '#email'
    )))
    # 텍스트 입력
    id_input.send_keys(ID)
    print("아이디 제출 성공")
except Exception as e:
    print("아이디 입력에 실패했습니다.")
    print(e)

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

try:
    submit_login_button = driver.find_element(By.CSS_SELECTOR,'#__next > main > section > div > div > div.css-1qjqoce > form > div:nth-child(1) > button')
    submit_login_button.click()
    print("로그인을 성공했습니다!")
except Exception as e:
    print("로그인에 실패했습니다...")
    print(e)

    #  직군 select
occupation_select_element = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > label:nth-child(1) > div > select'
)))

#  직무 select
job_select_element = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > label:nth-child(2) > div > select'
)))
#  경력 select
carrer_select_element = wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > label:nth-child(3) > div > select'
)))
apply_button= wait.until(EC.presence_of_element_located((
    By.CSS_SELECTOR,
    '#__next > main > section > article.FilterList_FilterList__0T9Zj > button'
)))

occupation_select = Select(occupation_select_element)
occupation_select.select_by_value(occupation_value)
job_select = Select(job_select_element)
job_select_options = job_select.options
carret_select = Select(carrer_select_element)
#carret_select.select_by_index(1) # 경력 연수가 신입 없는 직무가 존재함 (예: CTO)
# 직무 옵션 리스트 저장하기
for option in job_select_options[1:]:
    job_value_list.append(option.text)

def run_job_search():
    for job_value in range(len(job_value_list)):        
        try:    
            job_select.select_by_visible_text(job_value_list[job_value])
            carret_select.select_by_index(1)
            time.sleep(1)
            apply_button.click()
            print(f"{job_value_list[job_value]}직무 선택!")
            time.sleep(1)

            
        except Exception as e:
            print(f"{job_value_list[job_value]}에서 오류 발생 :{e}")
            continue
run_job_search()

# 결과 저장할 리스트
result = []

time.sleep(2)

for job_value in range(len(job_value_list)):        
    try:    
        job_select.select_by_visible_text(job_value_list[job_value])
        carret_select.select_by_index(1)
        time.sleep(1)
        apply_button.click()
        print(f"{job_value_list[job_value]} 직무 선택!")
        time.sleep(1)
        
        tech_stacks_element = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            '#__next > main > section > article.SkillInfo_SkillInfo__YSa5v > div:nth-child(2) > div.BarList_BarList__GvAW3'
        )))
        
        tech_stacks_text = tech_stacks_element.text.strip()

        if tech_stacks_text:
            lines = tech_stacks_text.split('\n')
            extracted_stacks = [line for line in lines if not any(char.isdigit() for char in line) and '%' not in line]
        else:
            extracted_stacks = None

        print(extracted_stacks)

        # ✅ 기술스택이 없어도 직무명은 저장, 기술스택은 None
        result.append({
            '직무': job_value_list[job_value],
            '기술스택': ', '.join(extracted_stacks) if extracted_stacks else None
        })

    except Exception as e:
        print(f"{job_value_list[job_value]}에서 오류 발생 : {e}")
        # ✅ 오류가 나도 직무명만이라도 기록!
        result.append({
            '직무': job_value_list[job_value],
            '기술스택': None
        })
        continue  # 오류나도 무조건 실행

# CSV 저장
df = pd.DataFrame(result)
df.to_csv('data/job_tech_stacks.csv', index=False, encoding='utf-8-sig') # 인코딩을 꼭 이걸로 해야 할까..
print("CSV 저장 완료!")