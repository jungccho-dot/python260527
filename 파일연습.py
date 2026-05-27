# 파일연습.py

# 파일 객체 생성
f = open("test.txt", "wt", encoding="utf-8")  # 쓰기 모드로 파일 열기
# 파일에 내용 쓰기
f.write("철번째라인\n두번째라인\n세번째라인\n")
# 파일 닫기
f.close()

# 파일 읽기
f = open("test.txt", "rt", encoding="utf-8")  # 읽기 모드로 파일 열기
content = f.read()  # 파일 전체 읽기
print(content)  # 파일 내용 출력
f.close()  # 파일 닫기


