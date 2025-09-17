import os
import glob

# 한글 글자들을 저장할 집합(set)을 생성합니다. 집합은 중복된 값을 허용하지 않습니다.
korean_characters = set()

# 검색할 파일 경로 패턴을 지정합니다.
path = "tmp/MessageData_translated/*.txt"

# 지정된 경로에 있는 모든 .txt 파일을 찾습니다.
files = glob.glob(path)

# 각 파일을 순회하며 내용을 읽고 한글을 추출합니다.
for file in files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            # 파일의 모든 내용을 하나의 문자열로 읽어옵니다.
            text = f.read()
            # 문자열의 각 글자를 확인합니다.
            for char in text:
                # 해당 글자가 한글 범위(가-힣)에 속하는지 확인합니다.
                if "가" <= char <= "힣":
                    # 한글이면 집합에 추가합니다.
                    korean_characters.add(char)
    except Exception as e:
        # 파일 읽기 중 오류가 발생하면 오류 메시지를 출력합니다.
        print(f"'{file}' 파일을 읽는 중 오류가 발생했습니다: {e}")

# 찾은 모든 한글 글자를 정렬하여 한 줄에 하나씩 출력합니다.
for char in sorted(list(korean_characters)):
    print(char)
