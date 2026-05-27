# DemoList.py

lst = [1,2,3,4,5]
print(len(lst))

lst.append(6)
print(lst)
lst.remove(3)
print(lst)

a = 'phthon'
# a[0:3]
print(a[0:3])

# 문자열 슬라이싱
strA = 'phthon'
strB = "파이썬은 강력해"
strC ="""다중 라인으로
저장하는
경우입니다."""

print(strC[-10:])

# Set형식

a = {1,2,3,4}
b = {3,4,4,5}
print(a)
print(b)
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

# Tuple
tp = (10,20,30)
print(tp[0])
print(tp.index(30))

def calc(a,b):
    return a+b, a*b

print(calc(3,4))
print("id: %s, name: %s" %("kim","김유신"))

# 형식변환
a = set((1,2,3))
print(a)
b = list(a)
print(b)
b.append(4)
print(b)