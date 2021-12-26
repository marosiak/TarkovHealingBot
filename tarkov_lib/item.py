class Item:
    position: tuple

    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f"Item at screen position: self.position"
