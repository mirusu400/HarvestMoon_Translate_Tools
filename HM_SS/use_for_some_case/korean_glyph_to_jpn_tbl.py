import os

try:
    # 한글 파일 읽기
    with open("koreans.txt", "r", encoding="utf-8") as f:
        # 각 줄의 앞뒤 공백/줄바꿈 문자를 제거하고 리스트로 저장
        korean_chars = [line.strip() for line in f]

    # 일본어 테이블 파일 읽기 및 새로운 한국어 테이블 파일 쓰기
    with open("ss_jpn.tbl", "r", encoding="utf-8") as f_jpn, open(
        "ss_kor.tbl", "w", encoding="utf-8"
    ) as f_kor:
        # 한글 리스트의 현재 위치를 추적하기 위한 변수
        korean_index = 0
        # 일본어 테이블 파일을 한 줄씩 읽기
        for line in f_jpn:
            # '=' 문자가 포함된 줄인지 확인
            if "=" in line:
                # 아직 사용할 한글이 남아있는지 확인
                if korean_index < len(korean_chars):
                    # '='를 기준으로 줄을 분리 (예: '88A3', '哀\n')
                    parts = line.split("=", 1)
                    hex_code = parts[0]

                    # 새로운 줄 생성 (예: '88A3' + '=' + '가' + '\n')
                    new_line = f"{hex_code}={korean_chars[korean_index]}\n"
                    f_kor.write(new_line)

                    # 다음 한글을 사용하기 위해 인덱스 1 증가
                    korean_index += 1
                else:
                    # 대체할 한글이 없으면 원본 줄을 그대로 씀
                    f_kor.write(line)
            else:
                # '=' 문자가 없는 줄은 그대로 씀
                f_kor.write(line)

    print("파일 변경이 완료되었습니다. 'ss_kor.tbl' 파일을 확인해주세요.")

except FileNotFoundError as e:
    print(
        f"오류: '{e.filename}' 파일을 찾을 수 없습니다. 파일이 코드와 같은 폴더에 있는지 확인해주세요."
    )
except Exception as e:
    print(f"알 수 없는 오류가 발생했습니다: {e}")
