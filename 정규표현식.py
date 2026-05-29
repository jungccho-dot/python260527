# 정규표현식.py
import re

result = re.search("[0-9]*th","1st 2nd 3rd 4th 5th 6th 7th 8th 9th 10th")
print(result)
print(result.group())

# result = re.match("[0-9]+th","1st 2nd 3rd 4th 5th 6th 7th 8th 9th 10th")
# print(result)
# print(result.group())

# 연도패턴
result = re.search("[0-9]{4}","올해는 2026년입니다.")
print(result.group())

# 전화번호 패턴
# result = re.search("[0-9]{3}-[0-9]{4}-[0-9]{4}","제 전화번호는 010-1234-5678입니다.")
result = re.search("\d{3}-\d{4}-\d{4}","제 전화번호는 010-1234-5678입니다.")
print(result.group())

# 이메일 패턴
result = re.search("[a-zA-Z0-9]+@[a-zA-Z0-9]+[.a-zA-Z]+","제 이메일 주소는 user@example.co.kr입니다.")
print(result.group())

# 우편번호 패턴
# result = re.search("[0-9]{5}","제 우편번호는 12345입니다.")
result = re.search("\d{5}","제 우편번호는 12345입니다.")
print(result.group())
