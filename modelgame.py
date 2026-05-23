import random

size = 10
shipshapes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hits = set()
    @property
    def is_sunk(self):
        return len(self.hits) == len(self.coordinates)
class ShipModel:
    def __init__(self):
        self.my_field = [[0] * size for _ in range(size)]
        self.enemy_field = [[0] * size for _ in range(size)]
        self.my_ships = []
        self.enemy_ships = []
        self.createships(self.enemy_field, self.enemy_ships)

    def availableplace(self, field, x, y, length, direction):
        for i in range(length):
            nx = x + (i if direction == 'H' else 0)
            ny = y + (0 if direction == 'H' else i)
            if not (0 <= nx < size and 0 <= ny < size):
                return False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    cx, cy = nx + dx, ny + dy
                    if 0 <= cx < size and 0 <= cy < size:
                        if field[cy][cx] == 1:
                            return False
        return True

    def createships(self, field, ships_list):
        for length in shipshapes:
            placed = False
            while not placed:
                direction = random.choice(['H', 'V'])
                x, y = random.randint(0, size - 1), random.randint(0, size - 1)
                if self.availableplace(field, x, y, length, direction):
                    coordinates = []
                    for i in range(length):
                        nx, ny = (x + i, y) if direction == 'H' else (x, y + i)
                        field[ny][nx] = 1
                        coordinates.append((nx, ny))
                    ships_list.append(Ship(coordinates))
                    placed = True

    def mark_shot(self, field, ships_list, x, y):
        if field[y][x] == 1:
            field[y][x] = 3
            for ship in ships_list:
                if (x, y) in ship.coordinates:
                    ship.hits.add((x, y))
                    if ship.is_sunk:
                        self.mark_around_sunk(field, ship)
                        for sx, sy in ship.coordinates:
                            field[sy][sx] = 4
                        return 'sink', ship
                    return 'hit', ship
        elif field[y][x] == 0:
            field[y][x] = 2
            return 'miss', None

        return 'already_shot', None

    def mark_around_sunk(self, field, ship):
        for (sx, sy) in ship.coordinates:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    cx, cy = sx + dx, sy + dy
                    if 0 <= cx < size and 0 <= cy < size:
                        if field[cy][cx] == 0:
                            field[cy][cx] = 2

    def check_victory(self, field):
        for row in field:
            if 1 in row:
                return False
        return True
