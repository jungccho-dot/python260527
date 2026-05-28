# DemoForm2.py
# DemoForm2.ui(화면단) + DemoForm2.py(로직단)으로 구성된 PyQt6 프로그램입니다.
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6 import uic
# 크롤링을 위한 선언
from bs4 import BeautifulSoup
# 웹서버에 요청
import urllib.request
# 정규표현식
import re


# 디자인 파일을 로딩
form_class = uic.loadUiType("DemoForm2.ui")[0]

# 폼클래스를 정의
class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
    # 슬롯메서드 정의
    def firstClick(self):
        #User-Agent를 조작하는 경우(아이폰에서 사용하는 사파리 브라우져의 헤더) 
        hdr = {'User-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/603.1.23 (KHTML, like Gecko) Version/10.0 Mobile/14E5239e Safari/602.1'}

        # 파일에 저장(write text)
        f = open("todayHumor.txt", "wt", encoding="utf-8")

        for i in range(1, 11):
            url = "https://www.todayhumor.co.kr/board/list.php?table=bestofbest&page=" + str(i)
            print("페이지 : " + url) # 페이지 번호 확인

            #웹브라우져 헤더 추가 
            req = urllib.request.Request(url, headers = hdr)
            data = urllib.request.urlopen(req).read()
            soup = BeautifulSoup(data, "html.parser")
            # 필터링 작업
            list = soup.find_all("td", attrs={"class":"subject"})
            for tag in list:
                title = tag.find("a").text.strip()
                # print(title) # 제목 확인
                # 문자열 검색(정규표현식)
                if re.search("한국", title):
                    print(title)
                    f.write(title + "\n")
            print("\n")
        f.close()
        self.label.setText("오늘의 유머 베스트 게시판 크롤링 완료!!")
    def secondClick(self):
        self.label.setText("두 번째 버튼이 클릭되었습니다!!!")
    def thirdClick(self):
        self.label.setText("세 번째 버튼이 클릭되었습니다!!~~~.")

# 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    demo = DemoForm()  # 폼 클래스의 인스턴스 생성
    demo.show()  # 폼을 화면에 표시
    sys.exit(app.exec())  # 이벤트 루프 시작