# 내장라이브러리.py
import random

print(random.random())  # 0.0 이상 1.0 미만의 랜덤한 실수 출력
print(random.random())  # 0.0 이상 1.0 미만의 랜덤한 실수 출력
# 구간을 지정
print(random.uniform(2.0, 20.0))  # 2.0 이상 20.0 미만의 랜덤한 실수 출력

# 리스트에서 랜덤하게 선택
fruits = ["사과", "바나나", "오렌지", "포도", "수박"]
print(random.choice(fruits))  # fruits 리스트에서 랜덤하게 하나 선택하여 출력

# 운영