"""
ProductDB 클래스 사용 예제 파일
"""
from ProductDB import ProductDB

def example_usage():
    """ProductDB 클래스의 다양한 사용 예제"""
    
    # 1. 데이터베이스 연결
    print("=" * 60)
    print("1. 데이터베이스 연결")
    print("=" * 60)
    db = ProductDB("MyProduct.db")
    
    # 2. 단일 제품 삽입
    print("\n" + "=" * 60)
    print("2. 새로운 제품 삽입")
    print("=" * 60)
    db.insert("LG 냉장고 AI", 2500000)
    db.insert("삼성 세탁기 스타일", 1800000)
    print("✓ 2개 제품 추가 완료")
    
    # 3. 여러 제품 일괄 삽입
    print("\n" + "=" * 60)
    print("3. 여러 제품 일괄 삽입")
    print("=" * 60)
    new_products = [
        ("구글 픽셀 7 Pro", 950000),
        ("아이폰 14 Pro Max", 1590000),
        ("삼성 갤럭시 Z Fold 5", 1980000)
    ]
    db.insert_many(new_products)
    print("✓ 3개 제품 일괄 추가 완료")
    
    # 4. 전체 제품 개수 조회
    print("\n" + "=" * 60)
    print("4. 전체 제품 개수")
    print("=" * 60)
    total_count = db.get_count()
    print(f"전체 제품: {total_count:,}개")
    
    # 5. ID로 제품 조회
    print("\n" + "=" * 60)
    print("5. ID로 제품 조회 (ID: 1)")
    print("=" * 60)
    product = db.select_by_id(1)
    if product:
        print(f"ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 6. 제품명으로 검색
    print("\n" + "=" * 60)
    print("6. 제품명 검색 (노트북)")
    print("=" * 60)
    notebooks = db.select_by_name("노트북")
    print(f"검색 결과: {len(notebooks)}개")
    print("처음 3개:")
    for product in notebooks[:3]:
        print(f"  ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 7. 가격 범위로 검색
    print("\n" + "=" * 60)
    print("7. 가격 범위 검색 (500,000 ~ 600,000원)")
    print("=" * 60)
    products_in_range = db.select_by_price_range(500000, 600000)
    print(f"검색 결과: {len(products_in_range)}개")
    print("처음 3개:")
    for product in products_in_range[:3]:
        print(f"  ID: {product[0]}, 이름: {product[1]}, 가격: {product[2]:,}원")
    
    # 8. UPDATE - 제품 가격 변경
    print("\n" + "=" * 60)
    print("8. 제품 정보 수정 (ID: 100)")
    print("=" * 60)
    old_product = db.select_by_id(100)
    print(f"수정 전: {old_product[1]}, {old_product[2]:,}원")
    
    db.update(100, product_price=2999000)
    new_product = db.select_by_id(100)
    print(f"수정 후: {new_product[1]}, {new_product[2]:,}원")
    
    # 9. UPDATE - 제품명 변경
    print("\n" + "=" * 60)
    print("9. 제품명 수정 (ID: 50)")
    print("=" * 60)
    old_product = db.select_by_id(50)
    print(f"수정 전: {old_product[1]}")
    
    db.update(50, product_name="프리미엄 울트라 게이밍 노트북")
    new_product = db.select_by_id(50)
    print(f"수정 후: {new_product[1]}")
    
    # 10. DELETE - 특정 제품 삭제
    print("\n" + "=" * 60)
    print("10. 제품 삭제 (ID: 2, 3, 4)")
    print("=" * 60)
    db.delete(2)
    db.delete(3)
    db.delete(4)
    print(f"현재 전체 제품: {db.get_count():,}개")
    
    # 11. 통계 조회
    print("\n" + "=" * 60)
    print("11. 데이터베이스 통계")
    print("=" * 60)
    stats = db.get_stats()
    print(f"총 제품 수: {stats['count']:,}개")
    print(f"최고 가격: {stats['max_price']:,}원")
    print(f"최저 가격: {stats['min_price']:,}원")
    print(f"평균 가격: {stats['avg_price']:,}원")
    
    # 12. 카테고리별 분석
    print("\n" + "=" * 60)
    print("12. 카테고리별 제품 검색")
    print("=" * 60)
    categories = ["스마트폰", "노트북", "태블릿", "카메라", "모니터"]
    for category in categories:
        count = len(db.select_by_name(category))
        print(f"{category}: {count:,}개")
    
    # 13. 고가 제품 조회
    print("\n" + "=" * 60)
    print("13. 고가 제품 상위 5개 (500,000원 이상)")
    print("=" * 60)
    high_price_products = db.select_by_price_range(500000, 1000000)
    print(f"500,000원 이상 제품: {len(high_price_products):,}개")
    print("상위 5개:")
    for product in high_price_products[:5]:
        print(f"  ID: {product[0]}, {product[1]}, {product[2]:,}원")
    
    # 데이터베이스 연결 종료
    db.close()
    print("\n" + "=" * 60)
    print("예제 실행 완료!")
    print("=" * 60)


if __name__ == "__main__":
    example_usage()
