# 클래스연습.py

class Person:
    def __init__(self):
        self.name = "default name"
    
    def print(self):
        print("My Name is {0}".format(self.name))

p1 = Person()
p2 = Person()
p2.name = "전우치"

p1.print()
p2.print()

