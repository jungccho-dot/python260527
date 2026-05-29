import os
import sqlite3
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

try:
    from openpyxl import Workbook
except ImportError:
    Workbook = None

DB_FILE = "Bycle.db"


def initialize_database():
    need_seed = False
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS Bycle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            qty INTEGER NOT NULL
        );
    """

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM Bycle;")
    count = cur.fetchone()[0]
    if count == 0:
        need_seed = True

    if need_seed:
        items = []
        for i in range(1, 101):
            bike_name = f"Bicycle {i:03d}"
            price = 120000 + (i % 20) * 5000
            qty = 1 + (i % 10)
            items.append((bike_name, price, qty))

        cur.executemany("INSERT INTO Bycle (name, price, qty) VALUES (?, ?, ?);", items)
        conn.commit()

    return conn


class BycleManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bycle 관리 앱")
        self.setMinimumSize(700, 520)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #eef2f7, stop:1 #d6e1f2);
                font-family: 'Malgun Gothic', 'Segoe UI', sans-serif;
                color: #2d3a4b;
            }
            QLineEdit {
                border: 1px solid #a0aec0;
                border-radius: 8px;
                padding: 8px;
                background: rgba(255, 255, 255, 0.95);
            }
            QLabel {
                font-size: 12pt;
                color: #2d3a4b;
            }
            QPushButton {
                border-radius: 10px;
                padding: 10px 18px;
                font-weight: 600;
                background-color: #4f7df5;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #2f69f0;
            }
            QPushButton:pressed {
                background-color: #1e54d6;
            }
            QTableWidget {
                border: 1px solid #a0aec0;
                background: white;
                gridline-color: #d8dce3;
            }
            QHeaderView::section {
                background-color: #4f7df5;
                color: white;
                padding: 8px;
                border: none;
                font-weight: 700;
            }
            QTableWidget::item:selected {
                background-color: #bdd7ff;
                color: #1d2a41;
            }
        """
)

        self.conn = initialize_database()
        self.cursor = self.conn.cursor()

        self.idEdit = QLineEdit()
        self.nameEdit = QLineEdit()
        self.priceEdit = QLineEdit()
        self.qtyEdit = QLineEdit()
        self.searchEdit = QLineEdit()

        self.idEdit.setPlaceholderText("ID")
        self.nameEdit.setPlaceholderText("자전거 이름")
        self.priceEdit.setPlaceholderText("가격")
        self.qtyEdit.setPlaceholderText("수량")
        self.searchEdit.setPlaceholderText("검색어(ID 또는 이름)")

        self.addButton = QPushButton("추가")
        self.updateButton = QPushButton("수정")
        self.deleteButton = QPushButton("삭제")
        self.excelButton = QPushButton("엑셀 출력")
        self.searchButton = QPushButton("검색")
        self.refreshButton = QPushButton("전체보기")

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "이름", "가격", "수량"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(1, self.table.horizontalHeader().ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, self.table.horizontalHeader().ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, self.table.horizontalHeader().ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, self.table.horizontalHeader().ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.addButton.clicked.connect(self.add_bycle)
        self.updateButton.clicked.connect(self.update_bycle)
        self.deleteButton.clicked.connect(self.delete_bycle)
        self.excelButton.clicked.connect(self.export_to_excel)
        self.searchButton.clicked.connect(self.search_bycle)
        self.refreshButton.clicked.connect(self.load_data)
        self.table.cellDoubleClicked.connect(self.load_selected_row)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel("ID"))
        form_layout.addWidget(self.idEdit)
        form_layout.addWidget(QLabel("이름"))
        form_layout.addWidget(self.nameEdit)
        form_layout.addWidget(QLabel("가격"))
        form_layout.addWidget(self.priceEdit)
        form_layout.addWidget(QLabel("수량"))
        form_layout.addWidget(self.qtyEdit)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.addWidget(self.addButton)
        button_layout.addWidget(self.updateButton)
        button_layout.addWidget(self.deleteButton)
        button_layout.addWidget(self.excelButton)
        button_layout.addStretch(1)
        button_layout.addWidget(self.searchEdit)
        button_layout.addWidget(self.searchButton)
        button_layout.addWidget(self.refreshButton)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.load_data()

    def show_message(self, title: str, text: str):
        QMessageBox.information(self, title, text)

    def load_data(self):
        self.table.setRowCount(0)
        search_text = self.searchEdit.text().strip()

        if search_text:
            if search_text.isdigit():
                query = "SELECT id, name, price, qty FROM Bycle WHERE id = ? OR name LIKE ? ORDER BY id"
                params = (int(search_text), f"%{search_text}%")
            else:
                query = "SELECT id, name, price, qty FROM Bycle WHERE name LIKE ? ORDER BY id"
                params = (f"%{search_text}%",)
        else:
            query = "SELECT id, name, price, qty FROM Bycle ORDER BY id"
            params = ()

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        self.table.setRowCount(len(rows))

        for row_index, row_data in enumerate(rows):
            id_item = QTableWidgetItem(str(row_data[0]))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(row_index, 0, id_item)

            name_item = QTableWidgetItem(row_data[1])
            self.table.setItem(row_index, 1, name_item)

            price_item = QTableWidgetItem(str(row_data[2]))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_index, 2, price_item)

            qty_item = QTableWidgetItem(str(row_data[3]))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row_index, 3, qty_item)

    def add_bycle(self):
        name = self.nameEdit.text().strip()
        price = self.priceEdit.text().strip()
        qty = self.qtyEdit.text().strip()

        if not name or not price.isdigit() or not qty.isdigit():
            self.show_message("입력 오류", "이름은 필수이며 가격과 수량은 숫자여야 합니다.")
            return

        self.cursor.execute(
            "INSERT INTO Bycle (name, price, qty) VALUES (?, ?, ?)",
            (name, int(price), int(qty)),
        )
        self.conn.commit()
        self.clear_inputs()
        self.load_data()

    def update_bycle(self):
        id_text = self.idEdit.text().strip()
        name = self.nameEdit.text().strip()
        price = self.priceEdit.text().strip()
        qty = self.qtyEdit.text().strip()

        if not id_text.isdigit() or not name or not price.isdigit() or not qty.isdigit():
            self.show_message("입력 오류", "ID, 이름, 가격, 수량을 모두 정확히 입력해 주세요.")
            return

        self.cursor.execute(
            "UPDATE Bycle SET name = ?, price = ?, qty = ? WHERE id = ?",
            (name, int(price), int(qty), int(id_text)),
        )
        if self.cursor.rowcount == 0:
            self.show_message("수정 실패", "해당 ID의 자전거를 찾을 수 없습니다.")
            return

        self.conn.commit()
        self.clear_inputs()
        self.load_data()

    def delete_bycle(self):
        id_text = self.idEdit.text().strip()
        if not id_text.isdigit():
            self.show_message("입력 오류", "삭제하려면 ID를 숫자로 입력하세요.")
            return

        self.cursor.execute("DELETE FROM Bycle WHERE id = ?", (int(id_text),))
        if self.cursor.rowcount == 0:
            self.show_message("삭제 실패", "해당 ID의 자전거를 찾을 수 없습니다.")
            return

        self.conn.commit()
        self.clear_inputs()
        self.load_data()

    def search_bycle(self):
        self.load_data()

    def clear_inputs(self):
        self.idEdit.clear()
        self.nameEdit.clear()
        self.priceEdit.clear()
        self.qtyEdit.clear()

    def export_to_excel(self):
        if Workbook is None:
            self.show_message("엑셀 저장 실패", "openpyxl 모듈이 설치되어 있지 않습니다. 먼저 pip install openpyxl 를 실행하세요.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "엑셀 파일로 저장", "BycleList.xlsx", "Excel Files (*.xlsx)")
        if not path:
            return

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Bycle 리스트"
        sheet.append(["ID", "이름", "가격", "수량"])

        self.cursor.execute("SELECT id, name, price, qty FROM Bycle ORDER BY id")
        for row_data in self.cursor.fetchall():
            sheet.append(row_data)

        workbook.save(path)
        self.show_message("엑셀 저장 완료", f"{os.path.basename(path)} 파일로 저장되었습니다.")

    def load_selected_row(self, row, column):
        self.idEdit.setText(self.table.item(row, 0).text())
        self.nameEdit.setText(self.table.item(row, 1).text())
        self.priceEdit.setText(self.table.item(row, 2).text())
        self.qtyEdit.setText(self.table.item(row, 3).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BycleManager()
    window.show()
    sys.exit(app.exec())
