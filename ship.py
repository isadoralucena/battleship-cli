class Ship:
    def __init__(self, positions):
        self._hit = False
        self._positions = positions
    
    @property
    def positions(self):
        return self._positions

    def hit_ship(self, x, y):
        if (x, y) in self._positions and not self._hit:
            self._hit = True
            return True
        return False