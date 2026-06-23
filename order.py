class Order:
    def __init__(self, id, items, amount):
        self.id = id
        self.items = [p.name for p in items]
        self.amount = amount
        self.status = "PENDING"
