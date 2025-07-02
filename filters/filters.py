# 시도코드 : 시 이름 딕셔너리
pension_sido_dict = {
    "11": "서울특별시",
    "26": "부산광역시",
    "27": "대구광역시",
    "28": "인천광역시",
    "29": "광주광역시",
    "30": "대전광역시",
    "31": "울산광역시",
    "36": "세종특별자치시",
    "41": "경기도",
    "43": "충청북도",
    "44": "충청남도",
    "45": "전라북도",
    "46": "전라남도",
    "47": "경상북도",
    "48": "경상남도",
    "50": "제주특별자치도",
    "51": "강원특별자치도",
    "52": "전북특별자치도"
}
# 가입자 수 기준으로 검색하는 기능 (원티드에 있는 수치 그대로 구현함)
def filter_employee_count(df, target):
    if target == "0":
        return df
    elif target == "50":
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
# 시 이름 기준으로 검색하는 기능
def filter_location(df, target_list):
    target_list = [int(x) for x in target_list]
    return df[df['법정동주소광역시도코드'].isin(target_list)]