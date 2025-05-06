# Evan-Soobin Jeon
# ejeon2@uci.edu

class Person:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Person: name={self.name}"

p = Person("Alice")
print(p)