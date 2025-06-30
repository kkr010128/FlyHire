import pandas as pd
import os
import re

# 1. 날짜를 지정
targetDate = "2506"

# 2. data 폴더에서 해당 날짜가 포함된 파일 찾기
for file in os.listdir("./raw_data"):
    if file.endswith(".csv") and re.search(r"(\d{6,8})", file) and targetDate in file:
        file_path = os.path.join("./raw_data", file)
        try:
            df = pd.read_csv(file_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding="cp949", low_memory=False)

        # 3. 필요한 열만 인덱스로 선택
        keep_indices = [1, 6, 9, 10, 11, 13, 14, 18, 19, 20, 21]
        df = df.iloc[:, keep_indices]

        # 4. 업종코드 필터링
        df = df[
            df.iloc[:, 5]
            .astype(str)
            .str.strip()
            .isin(
                [
                    "642004",  # 포털 및 기타 인터넷 정보 매개 서비스업
                    "721000",  # 컴퓨터 시스템 통합 자문, 구축 및 관리업 - 컴퓨터 시스템 통합(SI)자문 및 구축 서비스업
                    "722000",  # 시스템ㆍ응용 소프트웨어 개발 및 공급업
                    "722001",  # 게임 소프트웨어 개발 및 공급업 - 유선
                    "722002",  # 게임 소프트웨어 개발 및 공급업 - 모바일
                    "722003",  # 게임 소프트웨어 개발 및 공급업 - 기타 패키지
                    "722004",  # 시스템ㆍ응용 소프트웨어 개발 및 공급업 - 시스템 소프트웨어 개발 및 공급업
                    "722005",  # 컴퓨터 프로그래밍 서비스업
                    "723000",  # 자료 처리, 호스팅 및 관련 서비스업 - 호스팅 및 관련 서비스업
                    "723001",  # 자료 처리, 호스팅 및 관련 서비스업 - 자료 처리업
                    "724000",  # 데이터베이스 및 온라인 정보 제공업 (영상물 관련 스트리밍 서비스 등)
                    "729000",  # 기타 정보 기술 및 컴퓨터 운영 관련 서비스업
                ]
            )
        ]

        # 5. 저장
        output_path = f"./data/{targetDate}.csv"
        df.to_csv(output_path, index=False, encoding="utf-8-sig")
        print(f"{file} 불러옴")
        print(f"{output_path} 저장 완료")
        break
else:
    print(f"{targetDate}를 포함하는 CSV 파일 없음")
