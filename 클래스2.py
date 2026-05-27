# Person 클래스 (부모 클래스)
class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")

# Manager 클래스 (Person 상속)
class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title
    
    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")

# Employee 클래스 (Person 상속)
class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill
    
    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")

# 10개의 인스턴스 사용
manager1 = Manager(1, "홍길동", "개발팀 팀장")
manager2 = Manager(2, "김영희", "마케팅 팀장")

employee1 = Employee(3, "이순신", "파이썬")
employee2 = Employee(4, "세종대왕", "자바")
employee3 = Employee(5, "장보고", "C++")
employee4 = Employee(6, "이황", "웹개발")
employee5 = Employee(7, "강감찬", "데이터베이스")
employee6 = Employee(8, "을지문덕", "클라우드")
employee7 = Employee(9, "신사임당", "머신러닝")
employee8 = Employee(10, "정약용", "블록체인")

# 모든 인스턴스 정보 출력
print("=== Manager 정보 ===")
manager1.printInfo()
print()
manager2.printInfo()
print()

print("=== Employee 정보 ===")
employee1.printInfo()
print()
employee2.printInfo()
print()
employee3.printInfo()
print()
employee4.printInfo()
print()
employee5.printInfo()
print()
employee6.printInfo()
print()
employee7.printInfo()
print()
employee8.printInfo()
