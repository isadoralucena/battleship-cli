class Ship:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit = False

    @property
    def position(self):
        return self.x, self.y
    
    def hit_ship(self, x, y):
        if (self.x, self.y) == (x, y) and not self.hit:
            self.hit = True
            return True
        return False
