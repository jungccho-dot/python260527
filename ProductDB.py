import sqlite3
from typing import List, Tuple
import time

class ProductDB:
    """
    📦 전자제품 저장소 관리 클래스
    
    마치 장난감 상자처럼, 여러 전자제품들의 정보를 저장하고 찾고 수정하고 삭제할 수 있는 상자입니다.
    상자 안에는 제품의 이름, 번호, 가격 정보가 정리되어 있어요!
    
    예시:
    - 장난감 상자에 "스마트폰" "노트북" "이어폰" 같은 물건들이 들어있어요
    - 우리는 물건을 넣고(INSERT), 찾고(SELECT), 정보를 바꾸고(UPDATE), 버릴 수 있어요(DELETE)
    """
    
    def __init__(self, db_name: str = "MyProduct.db"):
        """
        🎁 전자제품 저장소를 새로 열기
        
        마치 새로운 상자를 꺼내서 열고, 그 안에 바구니를 만드는 것처럼
        데이터베이스 파일을 만들고 준비하는 작업입니다!
        
        :param db_name: 상자의 이름 (파일명)
                        기본값은 "MyProduct.db" 라는 이름의 상자를 만들어요
        
        예시:
            db = ProductDB("MyShop.db")  # "MyShop.db"라는 상자를 열어요
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_table()
    
    def connect(self):
        """
        🔗 저장소 문을 열기
        
        마치 냉장고 문을 열 듯이, 저장소에 접근할 수 있도록 문을 열어요.
        이제 안에 있는 물건들을 보고 꺼낼 수 있어요!
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f"✓ 데이터베이스 '{self.db_name}' 연결 완료")
        except sqlite3.Error as e:
            print(f"✗ 데이터베이스 연결 오류: {e}")
    
    def create_table(self):
        """
        📋 저장소 안에 정리함 만들기
        
        냉장고 안에 김치통, 반찬통처럼 물건들을 정리할 상자를 만드는 거예요.
        여기서는 "Products" 라는 정리함을 만들어요.
        이 정리함에는 제품ID, 제품이름, 제품가격을 써서 보관할 거에요!
        """
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY AUTOINCREMENT,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                )
            """)
            self.conn.commit()
            print("✓ Products 테이블 생성/확인 완료")
        except sqlite3.Error as e:
            print(f"✗ 테이블 생성 오류: {e}")
    
    def insert(self, product_name: str, product_price: int) -> bool:
        """
        🎯 장난감 상자에 물건 하나 넣기
        
        냉장고에 반찬 하나를 넣는 것처럼, 저장소에 제품 정보 하나를 추가해요.
        제품의 이름과 가격을 알려주면 자동으로 번호도 매겨져요!
        
        :param product_name: 제품의 이름 (예: "아이폰", "노트북")
        :param product_price: 제품의 가격 (예: 100000 원)
        :return: 성공하면 True, 실패하면 False를 돌려줘요
        
        예시:
            db.insert("스마트폰", 500000)  # 스마트폰을 50만원에 추가!
        """
        try:
            self.cursor.execute(
                "INSERT INTO Products (productName, productPrice) VALUES (?, ?)",
                (product_name, product_price)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ INSERT 오류: {e}")
            return False
    
    def insert_many(self, products: List[Tuple[str, int]]) -> bool:
        """
        🚚 여러 개의 물건을 한 번에 넣기
        
        냉장고에 한 번에 10개의 반찬을 넣는 것처럼,
        여러 제품의 정보를 한 번에 빠르게 저장소에 추가해요!
        한 개씩 넣는 것보다 훨씬 빨라요!
        
        :param products: [(이름, 가격), (이름, 가격), ...] 형태의 리스트
                        여러 제품 정보가 들어있는 상자들의 모음이에요
        :return: 성공하면 True, 실패하면 False를 돌려줘요
        
        예시:
            items = [("스마트폰", 500000), ("노트북", 1000000)]
            db.insert_many(items)  # 2개를 동시에 추가!
        """
        try:
            self.cursor.executemany(
                "INSERT INTO Products (productName, productPrice) VALUES (?, ?)",
                products
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"✗ INSERT MANY 오류: {e}")
            return False
    
    def select_all(self) -> List[Tuple]:
        """
        👀 저장소에 들어있는 모든 물건 보기
        
        마치 냉장고를 쭉 열어서 안에 뭐가 있는지 다 보는 것처럼,
        저장소에 들어있는 모든 제품들을 보여줘요!
        각 제품마다 (번호, 이름, 가격)이 함께 나와요.
        
        :return: [(번호, 이름, 가격), (번호, 이름, 가격), ...] 형태의 리스트
        
        예시:
            all_products = db.select_all()
            for product in all_products:
                print(f"번호: {product[0]}, 이름: {product[1]}, 가격: {product[2]}")
        """
        try:
            self.cursor.execute("SELECT * FROM Products ORDER BY productID")
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ SELECT 오류: {e}")
            return []
    
    def select_by_id(self, product_id: int) -> Tuple:
        """
        🔍 번호로 물건 찾기
        
        마치 도서관에서 "1번 책 주세요~"라고 말하면 그 책을 찾아주는 것처럼,
        제품의 번호를 알려주면 그 제품의 모든 정보를 찾아줘요!
        
        :param product_id: 찾고 싶은 제품의 번호
        :return: 찾으면 (번호, 이름, 가격)을 돌려줘요, 없으면 None이라고 알려줘요
        
        예시:
            product = db.select_by_id(1)  # 1번 제품을 찾아!
            # 결과: (1, "스마트폰", 500000)
        """
        try:
            self.cursor.execute(
                "SELECT * FROM Products WHERE productID = ?",
                (product_id,)
            )
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"✗ SELECT BY ID 오류: {e}")
            return None
    
    def select_by_name(self, product_name: str) -> List[Tuple]:
        """
        🏷️ 이름으로 물건 찾기
        
        마치 "스마트폰 있어?" 하고 물어보면 모든 스마트폰을 찾아주는 것처럼,
        제품의 이름이 포함된 모든 제품들을 찾아줘요!
        (예: "노트북"을 검색하면 "삼성 노트북", "LG 노트북" 등이 모두 나와요)
        
        :param product_name: 찾고 싶은 제품의 이름 (부분적으로만 말해도 돼요!)
        :return: 찾은 제품들의 리스트
        
        예시:
            notebooks = db.select_by_name("노트북")  # 노트북이라는 이름이 들어간 모든 제품!
            # 결과: [(2, "삼성 노트북", 1000000), (3, "LG 노트북", 900000), ...]
        """
        try:
            self.cursor.execute(
                "SELECT * FROM Products WHERE productName LIKE ? ORDER BY productID",
                (f"%{product_name}%",)
            )
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ SELECT BY NAME 오류: {e}")
            return []
    
    def select_by_price_range(self, min_price: int, max_price: int) -> List[Tuple]:
        """
        💰 가격이 비슷한 물건들 찾기
        
        마치 "1,000원부터 3,000원짜리 장난감 주세요~"라고 하면
        그 가격대의 장난감들을 다 찾아주는 것처럼,
        가격 범위 안에 있는 모든 제품들을 찾아줘요!
        
        :param min_price: 최소 가격 (가장 싼 가격)
        :param max_price: 최대 가격 (가장 비싼 가격)
        :return: 그 가격 범위에 있는 모든 제품들의 리스트
        
        예시:
            cheap_items = db.select_by_price_range(100000, 500000)
            # 10만원부터 50만원 사이의 모든 제품을 찾아!
        """
        try:
            self.cursor.execute(
                "SELECT * FROM Products WHERE productPrice BETWEEN ? AND ? ORDER BY productPrice",
                (min_price, max_price)
            )
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"✗ SELECT BY PRICE RANGE 오류: {e}")
            return []
    
    def update(self, product_id: int, product_name: str = None, product_price: int = None) -> bool:
        """
        ✏️ 이미 있는 물건의 정보 바꾸기
        
        냉장고에 있던 반찬을 꺼내서 "어, 이건 상한 것 같은데?"해서
        새로운 반찬으로 바꾸는 것처럼, 이미 저장되어 있는 제품의
        정보(이름이나 가격)를 새로운 정보로 바꿔줘요!
        
        :param product_id: 수정하고 싶은 제품의 번호
        :param product_name: 새로운 제품 이름 (안 바꾸려면 None)
        :param product_price: 새로운 제품 가격 (안 바꾸려면 None)
        :return: 성공하면 True, 실패하면 False를 돌려줘요
        
        예시:
            db.update(1, product_price=600000)  # 1번 제품의 가격을 60만원으로 바꿔!
            db.update(5, product_name="새로운 이름")  # 5번 제품의 이름만 바꿔!
        """
        try:
            # 기존 데이터 조회
            current = self.select_by_id(product_id)
            if not current:
                print(f"✗ ID {product_id}인 제품이 없습니다")
                return False
            
            # None 값은 기존 값으로 유지
            new_name = product_name if product_name is not None else current[1]
            new_price = product_price if product_price is not None else current[2]
            
            self.cursor.execute(
                "UPDATE Products SET productName = ?, productPrice = ? WHERE productID = ?",
                (new_name, new_price, product_id)
            )
            self.conn.commit()
            print(f"✓ ID {product_id} 제품 업데이트 완료")
            return True
        except sqlite3.Error as e:
            print(f"✗ UPDATE 오류: {e}")
            return False
    
    def delete(self, product_id: int) -> bool:
        """
        🗑️ 물건 하나 버리기
        
        냉장고에 들어있는 상한 반찬을 꺼내서 버리는 것처럼,
        저장소에 있는 제품 정보 하나를 삭제해줘요!
        
        :param product_id: 버리고 싶은 제품의 번호
        :return: 성공하면 True (정말로 지워졌어!), 실패하면 False (그런 번호가 없어)
        
        예시:
            db.delete(3)  # 3번 제품을 저장소에서 삭제!
        """
        try:
            self.cursor.execute("DELETE FROM Products WHERE productID = ?", (product_id,))
            self.conn.commit()
            if self.cursor.rowcount > 0:
                print(f"✓ ID {product_id} 제품 삭제 완료")
                return True
            else:
                print(f"✗ ID {product_id}인 제품이 없습니다")
                return False
        except sqlite3.Error as e:
            print(f"✗ DELETE 오류: {e}")
            return False
    
    def delete_all(self) -> bool:
        """
        🧹 냉장고 안의 모든 물건 버리기
        
        냉장고 안의 모든 반찬을 한 번에 치워버리는 것처럼,
        저장소에 있는 모든 제품 정보를 한 번에 삭제해줘요!
        주의! 한 번 지우면 다시 돌아오지 않아요!
        
        :return: 성공하면 True, 실패하면 False를 돌려줘요
        
        예시:
            db.delete_all()  # 모든 제품을 삭제! (정말 신중하게!)
        """
        try:
            self.cursor.execute("DELETE FROM Products")
            self.conn.commit()
            print(f"✓ 모든 제품 삭제 완료 (삭제된 행: {self.cursor.rowcount})")
            return True
        except sqlite3.Error as e:
            print(f"✗ DELETE ALL 오류: {e}")
            return False
    
    def get_count(self) -> int:
        """
        🔢 저장소에 몇 개의 물건이 있는지 세기
        
        냉장고를 열어서 "어, 반찬이 몇 개 있지?" 하고 세는 것처럼,
        저장소에 총 몇 개의 제품이 있는지 알려줘요!
        
        :return: 저장소에 있는 모든 제품의 개수
        
        예시:
            count = db.get_count()  # 저장소에 몇 개가 있어?
            print(f"총 {count}개의 제품이 있어요!")  # 총 100,000개의 제품이 있어요!
        """
        try:
            self.cursor.execute("SELECT COUNT(*) FROM Products")
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"✗ COUNT 오류: {e}")
            return 0
    
    def get_stats(self) -> dict:
        """
        📊 저장소의 제품들에 대한 재미있는 정보 보기
        
        마치 "냉장고 안의 반찬들 중에 가장 비싼 건 뭐고, 가장 싼 건 뭐야?"
        같은 질문에 대답하듯, 제품들에 대한 여러 정보를 한 번에 알려줘요!
        
        :return: {'count': 총 개수,
                  'max_price': 가장 비싼 제품의 가격,
                  'min_price': 가장 싼 제품의 가격,
                  'avg_price': 모든 제품 가격의 평균}
        
        예시:
            stats = db.get_stats()
            print(f"총 {stats['count']}개 제품이 있어요!")
            print(f"가장 비싼 제품: {stats['max_price']}원")
            print(f"가장 싼 제품: {stats['min_price']}원")
            print(f"평균 가격: {stats['avg_price']}원")
        """
        try:
            self.cursor.execute(
                "SELECT COUNT(*), MAX(productPrice), MIN(productPrice), AVG(productPrice) FROM Products"
            )
            count, max_p, min_p, avg_p = self.cursor.fetchone()
            return {
                'count': count if count else 0,
                'max_price': max_p if max_p else 0,
                'min_price': min_p if min_p else 0,
                'avg_price': round(avg_p, 2) if avg_p else 0
            }
        except sqlite3.Error as e:
            print(f"✗ 통계 조회 오류: {e}")
            return {}
    
    def close(self):
        """
        🚪 저장소 문 닫기
        
        모든 일이 끝났으니 냉장고 문을 닫는 것처럼,
        저장소와의 연결을 종료해줘요.
        작업이 끝나면 꼭 이 함수를 호출해야 해요!
        
        예시:
            # 모든 작업 완료!
            db.close()  # 문을 닫아!
        """
        if self.conn:
            self.conn.close()
            print("✓ 데이터베이스 연결 종료")


def generate_sample_data(count: int = 100000) -> List[Tuple[str, int]]:
    """
    🎲 테스트할 샘플 제품들 만들기
    
    마치 레고 블록을 조합해서 여러 모양을 만드는 것처럼,
    우리가 저장소에 넣을 연습용 제품들을 만들어줘요!
    기본적으로 10만 개의 가짜 제품들을 만들어요.
    
    이렇게 만들어진 데이터는 "삼성 스마트폰 Pro", "LG 노트북 Max" 처럼
    실제로 있을 법한 제품들이에요!
    
    :param count: 몇 개의 샘플 제품을 만들 건지 (기본값: 100,000개)
    :return: [(제품이름, 가격), (제품이름, 가격), ...] 형태의 리스트
    
    예시:
        # 기본 10만 개 만들기
        data = generate_sample_data()
        
        # 1000개만 만들기
        small_data = generate_sample_data(1000)
    """
    product_categories = [
        "스마트폰", "노트북", "태블릿", "이어폰", "마우스",
        "키보드", "모니터", "프린터", "카메라", "스피커",
        "헤드폰", "외장HDD", "USB", "충전기", "케이블",
        "라우터", "무선마우스", "웹캠", "마이크", "게이밍헤드셋"
    ]
    
    product_models = [
        "Pro", "Max", "Ultra", "Standard", "Lite", "Plus",
        "X", "Z", "V", "S", "SE", "Air", "Touch", "Mini"
    ]
    
    product_brands = [
        "Samsung", "LG", "Apple", "Sony", "Dell", "HP",
        "ASUS", "Canon", "Nikon", "Lenovo", "Xiaomi", "Anker"
    ]
    
    data = []
    for i in range(count):
        category = product_categories[i % len(product_categories)]
        model = product_models[(i // len(product_categories)) % len(product_models)]
        brand = product_brands[(i // (len(product_categories) * len(product_models))) % len(product_brands)]
        
        product_name = f"{brand} {category} {model}"
        product_price = 10000 + (i * 100) % 1000000  # 10,000 ~ 1,000,000 범위
        
        data.append((product_name, product_price))
    
    return data


if __name__ == "__main__":
    print("=" * 60)
    print("SQLite 전자제품 데이터베이스 관리 프로그램")
    print("=" * 60)
    
    # 데이터베이스 초기화
    db = ProductDB("MyProduct.db")
    
    # 기존 데이터가 있으면 삭제
    existing_count = db.get_count()
    if existing_count > 0:
        print(f"\n기존 데이터 {existing_count}개를 삭제합니다...")
        db.delete_all()
    
    # 샘플 데이터 생성 및 삽입
    print("\n샘플 데이터 생성 중... (10만 개)")
    start_time = time.time()
    sample_data = generate_sample_data(100000)
    
    print("데이터베이스에 삽입 중...")
    db.insert_many(sample_data)
    end_time = time.time()
    
    print(f"✓ 삽입 완료 ({end_time - start_time:.2f}초)")
    
    # 통계 정보 출력
    print("\n" + "=" * 60)
    print("데이터베이스 통계")
    print("=" * 60)
    stats = db.get_stats()
    print(f"총 제품 개수: {stats['count']:,}개")
    print(f"최고 가격: {stats['max_price']:,}원")
    print(f"최저 가격: {stats['min_price']:,}원")
    print(f"평균 가격: {stats['avg_price']:,}원")
    
    # 샘플 조회 - 처음 5개
    print("\n" + "=" * 60)
    print("처음 5개 제품 정보")
    print("=" * 60)
    all_products = db.select_all()[:5]
    for product in all_products:
        print(f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 샘플 검색 - 스마트폰
    print("\n" + "=" * 60)
    print("스마트폰 검색 결과 (처음 5개)")
    print("=" * 60)
    smartphone = db.select_by_name("스마트폰")[:5]
    for product in smartphone:
        print(f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 샘플 UPDATE - ID 1 제품 가격 변경
    print("\n" + "=" * 60)
    print("UPDATE 테스트")
    print("=" * 60)
    print("ID 1 제품 가격을 999,999원으로 변경합니다")
    db.update(1, product_price=999999)
    updated = db.select_by_id(1)
    print(f"변경 후: ID: {updated[0]}, 이름: {updated[1]}, 가격: {updated[2]:,}원")
    
    # 샘플 DELETE - ID 5 제품 삭제
    print("\n" + "=" * 60)
    print("DELETE 테스트")
    print("=" * 60)
    print("ID 5 제품을 삭제합니다")
    db.delete(5)
    
    # 가격 범위 검색
    print("\n" + "=" * 60)
    print("가격 범위 검색 (100,000~150,000원)")
    print("=" * 60)
    price_range_products = db.select_by_price_range(100000, 150000)[:5]
    print(f"검색 결과: {len(db.select_by_price_range(100000, 150000))}개")
    print("처음 5개:")
    for product in price_range_products:
        print(f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 최종 통계
    print("\n" + "=" * 60)
    print("최종 데이터베이스 통계")
    print("=" * 60)
    final_stats = db.get_stats()
    print(f"총 제품 개수: {final_stats['count']:,}개")
    
    # 데이터베이스 종료
    db.close()
    print("\n프로그램 종료")
