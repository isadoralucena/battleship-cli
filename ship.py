class Ship:
    def __init__(self, positions):
        self._positions = positions
        self._hit = [False] * len(positions)
    
    @property
    def positions(self):
        return self._positions
    
    @property
    def hit(self):
        return all(self._hit)

    def register_hit(self, x, y):
        for i, pos in enumerate(self._positions):
            if pos == (x, y) and not self._hit[i]:
                self._hit[i] = True
                return True
        return False