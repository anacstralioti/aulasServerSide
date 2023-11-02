class Customer:
    def __init__(self, id = 0, name = "no name"):
        self.id = id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name}