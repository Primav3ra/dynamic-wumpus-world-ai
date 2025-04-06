
class BaseAgent:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x
        self.y = y
        self.alive = True
        self.has_gold = False
        self.direction = "E"  # N, E, S, W
        self.arrow_count = 1
        self.memory = set()

    def current_position(self):
        return self.x, self.y

    def turn_left(self):
        directions = ["N", "W", "S", "E"]
        idx = directions.index(self.direction)
        self.direction = directions[(idx + 1) % 4]

    def turn_right(self):
        directions = ["N", "E", "S", "W"]
        idx = directions.index(self.direction)
        self.direction = directions[(idx + 1) % 4]

    def move_forward(self):
        if self.direction == "N":
            self.y -= 1
        elif self.direction == "S":
            self.y += 1
        elif self.direction == "E":
            self.x += 1
        elif self.direction == "W":
            self.x -= 1

    def record_memory(self, perception):
        self.memory.add((self.x, self.y, tuple(perception.as_list())))
