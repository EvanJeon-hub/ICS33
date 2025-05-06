class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f"User(id={self.id}, name='{self.name}')"

    def __repr__(self):
        return self.__str__()



users = [User(1, '철수'), User(2, '영희')]
print(users)