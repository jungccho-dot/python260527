# SQLite 전자제품 데이터베이스 관리 시스템

## 📋 프로젝트 개요

SQLite를 사용하여 전자제품 데이터를 효율적으로 관리하는 Python 클래스 기반 데이터베이스 시스템입니다.
- **데이터베이스**: MyProduct.db (3.1MB, 10만 개 제품 데이터)
- **테이블명**: Products
- **프로그래밍 방식**: 클래스 메서드 기반 CRUD 작업

---

## 📁 파일 구조

```
c:\work\
├── ProductDB.py                 # 메인 클래스 및 데이터 생성
├── ProductDB_Example.py         # 사용 예제 파일
├── MyProduct.db                 # SQLite 데이터베이스 파일
└── 이 README.md                 # 사용 가이드
```

---

## 🗄️ 데이터베이스 스키마

### Products 테이블

| 컬럼명 | 타입 | 설명 | 속성 |
|--------|------|------|------|
| productID | INTEGER | 제품 ID | PRIMARY KEY, AUTOINCREMENT |
| productName | TEXT | 제품명 | NOT NULL |
| productPrice | INTEGER | 제품 가격 (원) | NOT NULL |

---

## 🚀 ProductDB 클래스 메서드

### 1. **초기화 및 연결**

```python
from ProductDB import ProductDB

# 데이터베이스 초기화 및 연결
db = ProductDB("MyProduct.db")
```

### 2. **INSERT - 데이터 삽입**

#### 단일 제품 삽입
```python
db.insert("LG 냉장고 AI", 2500000)
# 반환값: True (성공) / False (실패)
```

#### 여러 제품 일괄 삽입
```python
products = [
    ("구글 픽셀 7 Pro", 950000),
    ("아이폰 14 Pro Max", 1590000),
    ("삼성 갤럭시 Z Fold 5", 1980000)
]
db.insert_many(products)
```

---

### 3. **SELECT - 데이터 조회**

#### 모든 제품 조회
```python
all_products = db.select_all()
for product in all_products[:5]:  # 처음 5개
    print(f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]}")
```

#### ID로 특정 제품 조회
```python
product = db.select_by_id(1)
# 반환값: (productID, productName, productPrice) 또는 None
```

#### 제품명으로 검색 (부분 일치)
```python
notebooks = db.select_by_name("노트북")
print(f"검색 결과: {len(notebooks)}개")
```

#### 가격 범위로 검색
```python
products = db.select_by_price_range(500000, 1000000)
# 500,000 ~ 1,000,000원 범위의 제품 조회
```

---

### 4. **UPDATE - 데이터 수정**

#### 제품 가격 변경
```python
db.update(1, product_price=999999)
# ID 1인 제품의 가격을 999,999원으로 변경
```

#### 제품명 변경
```python
db.update(50, product_name="프리미엄 게이밍 노트북")
```

#### 제품명과 가격 동시 변경
```python
db.update(100, product_name="삼성 최신형", product_price=2500000)
```

---

### 5. **DELETE - 데이터 삭제**

#### 특정 제품 삭제
```python
db.delete(5)  # ID 5인 제품 삭제
```

#### 모든 제품 삭제 (주의!)
```python
db.delete_all()  # 모든 제품 삭제
```

---

### 6. **통계 및 정보 조회**

#### 전체 제품 개수
```python
count = db.get_count()
print(f"전체 제품: {count:,}개")
```

#### 통계 정보 조회
```python
stats = db.get_stats()
print(f"총 개수: {stats['count']:,}개")
print(f"최고 가격: {stats['max_price']:,}원")
print(f"최저 가격: {stats['min_price']:,}원")
print(f"평균 가격: {stats['avg_price']:,}원")
```

---

### 7. **데이터베이스 연결 종료**

```python
db.close()  # 데이터베이스 연결 종료
```

---

## 💻 실행 방법

### 메인 프로그램 실행 (10만 개 데이터 생성)
```bash
python ProductDB.py
```
- MyProduct.db 데이터베이스 생성
- 10만 개의 샘플 데이터 자동 생성 및 삽입
- 각 기능 테스트 실행

### 사용 예제 실행
```bash
python ProductDB_Example.py
```
- INSERT, SELECT, UPDATE, DELETE 실제 사용 예제
- 통계 조회 및 검색 기능 시연

---

## 📊 샘플 데이터 특징

### 제품 분류
- **카테고리**: 스마트폰, 노트북, 태블릿, 이어폰, 마우스, 키보드 등 (20개 카테고리)
- **브랜드**: Samsung, LG, Apple, Sony, Dell, HP, ASUS 등 (12개 브랜드)
- **모델**: Pro, Max, Ultra, Standard, Lite, Plus, X, Z, V, S, SE, Air, Touch, Mini

### 가격 범위
- **최저가**: 10,000원
- **최고가**: 1,009,900원
- **평균가**: 약 510,000원

### 데이터 총량
- **제품 수**: 100,000개
- **파일 크기**: 약 3.1MB
- **삽입 시간**: 약 0.12초 (빠른 성능)

---

## 🔍 사용 시나리오 예제

### 시나리오 1: 50만원대 제품 찾기
```python
db = ProductDB("MyProduct.db")
products = db.select_by_price_range(500000, 600000)
print(f"50만원대 제품: {len(products)}개 발견")

for product in products[:5]:
    print(f"  {product[1]} - {product[2]:,}원")
db.close()
```

### 시나리오 2: 스마트폰 제품 가격 인상
```python
db = ProductDB("MyProduct.db")
smartphones = db.select_by_name("스마트폰")
print(f"총 {len(smartphones)}개 스마트폰")

# 처음 10개의 가격을 10% 인상
for phone in smartphones[:10]:
    new_price = int(phone[2] * 1.1)
    db.update(phone[0], product_price=new_price)
db.close()
```

### 시나리오 3: 가장 비싼 상품 찾기
```python
db = ProductDB("MyProduct.db")
stats = db.get_stats()
max_price = stats['max_price']

expensive = db.select_by_price_range(max_price - 100000, max_price)
print(f"가장 비싼 상품 TOP 5:")
for product in expensive[:5]:
    print(f"  {product[1]} - {product[2]:,}원")
db.close()
```

---

## ⚙️ 주요 특징

✅ **효율적인 데이터 처리**
- SQLite 데이터베이스로 빠른 조회 및 수정
- executemany()를 사용한 고속 대량 삽입 (0.12초)

✅ **직관적인 메서드 기반 인터페이스**
- insert(), update(), delete(), select_*() 등 명확한 메서드명

✅ **다양한 검색 기능**
- ID 검색, 제품명 검색, 가격 범위 검색

✅ **통계 및 분석 기능**
- 전체 개수, 최고/최저/평균 가격 조회

✅ **에러 처리**
- 모든 메서드에 예외 처리 포함
- 작업 결과를 사용자에게 명확히 표시

---

## 🐛 트러블슈팅

### Q: "database is locked" 오류 발생
**A**: 여러 프로세스가 동시에 접근하지 않도록 주의하세요. 필요시 `close()` 호출 후 재연결하세요.

### Q: 데이터베이스 파일이 계속 커지는 문제
**A**: SQLite는 삭제된 공간을 재활용합니다. `VACUUM` 명령어로 최적화할 수 있습니다.

### Q: 조회가 느려질 때
**A**: 자주 검색하는 컬럼에 인덱스를 추가하면 성능이 향상됩니다.

---

## 📝 라이선스

이 코드는 학습 목적으로 자유롭게 사용할 수 있습니다.

---

**작성일**: 2026년 5월 27일  
**Python 버전**: 3.7 이상  
**필수 라이브러리**: sqlite3 (표준 라이브러리)
