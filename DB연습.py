# DB연습.py
import sqlite3

# 데이터베이스 연결 (없으면 새로 생성)
# conn = sqlite3.connect("c:\\work\\test.db")
conn = sqlite3.connect(":memory:")  # 메모리 상에서 임시 데이터베이스 생성
# 커서 객체 생성
cursor = conn.cursor()

# 테이블 생성 (이미 존재하면 무시)
cursor.execute("CREATE TABLE IF NOT EXISTS PhonBook (Name text, PhoneNum text)")
# 데이터 삽입
cursor.execute("INSERT INTO PhonBook VALUES ('홍길동', '010-1234-5678')")
cursor.execute("INSERT INTO PhonBook VALUES ('김영희', '010-9876-5432')")
# 입력 파라미터로 데이터 삽입
name = "이순신"
phone = "010-5555-6666"
cursor.execute("INSERT INTO PhonBook VALUES (?, ?)", (name, phone))
# 여러건을 한 번에 삽입
data = [("세종대왕", "010-1111-2222"), ("장보고", "010-3333-4444")]
cursor.executemany("INSERT INTO PhonBook VALUES (?, ?)", data)

# 데이터 조회
for row in cursor.execute("SELECT * FROM PhonBook"):
    print(row)
# 데이터베이스 연결 종료
conn.close()
