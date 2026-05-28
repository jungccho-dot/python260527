# DemoForm.py
# DemoForm.ui(화면단) + DemoForm.py(로직단)으로 구성된 PyQt6 프로그램입니다.
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt6 import uic

# 디자인 파일을 로딩
form_class = uic.loadUiType("DemoForm.ui")[0]

# 폼클래스를 정의
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.label.setText("이렇게 화면에 출력!")

# 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    demo = DemoForm()  # 폼 클래스의 인스턴스 생성
    demo.show()  # 폼을 화면에 표시
    sys.exit(app.exec())  # 이벤트 루프 시작