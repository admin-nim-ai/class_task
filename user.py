class User:
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role


class Admin(User):
    def __init__(self, id, name):
        super().__init__(id, name, "admin")


class Customer(User):
    def __init__(self, id, name):
        super().__init__(id, name, "customer")
