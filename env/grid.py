
import random
from env.tile import Tile
from .perception import Perception

GRID_SIZE = 8
PIT_PROBABILITY = 0.2

class Grid:
    def __init__(self, size=8):
        self.size = size
        self.grid = [[Tile(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.generate_world()

    def generate_world(self):
        all_coords = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) != (0, 0)]
        random.shuffle(all_coords)

        #1 Wumpus
        wumpus_x, wumpus_y = all_coords.pop()
        self.grid[wumpus_y][wumpus_x].has_wumpus = True

        #1 Gold
        gold_x, gold_y = all_coords.pop()
        self.grid[gold_y][gold_x].has_gold = True

        #4 to 6 pits
        num_pits = random.randint(4, 6)
        for _ in range(num_pits):
            pit_x, pit_y = all_coords.pop()
            self.grid[pit_y][pit_x].has_pit = True


    def print_grid(self, player=None, wumpus=None):
        print("\nWumpus World:")
        print("+" + "---+" * self.size)
        for y in range(self.size):
            row = "|"
            for x in range(self.size):
               tile = self.tiles[y][x]
               char = "."

            if player and player.x == x and player.y == y:
                char = "P"
            elif wumpus and wumpus.x == x and wumpus.y == y:
                char = "W"
            elif tile.has_gold:
                char = "G"
            elif tile.has_pit:
                char = "O"

            row += f" {char} |"
        print(row)
        print("+" + "---+" * self.size)

    

#plugging in perception into the grid next so these agents can start thinking.
#method that scans adjacent tiles to generate Perception for any agent.


    def get_perception(self, x, y, is_player=True):
        stench = False
        breeze = False
        glitter = False
        bump = False
        scream = False
        sees_player = False

        # Check adjacent tiles
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                neighbor = self.grid[ny][nx]
                if neighbor.has_wumpus and is_player:
                    stench = True
                if neighbor.has_player and not is_player:
                    sees_player = True
                if neighbor.has_pit:
                    breeze = True

        # Check current tile
        current = self.grid[y][x]
        if current.has_gold:
            glitter = True
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            bump = True

        return Perception(
            stench=stench,
            breeze=breeze,
            glitter=glitter,
            bump=bump,
            scream=scream,
            sees_player=sees_player
        )


#THE OLD CODE 

    '''   self.place_pits()
        self.place_gold()
        self.place_wumpus()
        self.place_player() 

    def place_pits(self):
        for row in self.grid:
            for tile in row:
                if (tile.x, tile.y) != (0, 0):
                    tile.has_pit = random.random() < PIT_PROBABILITY

    def place_gold(self):
        while True:
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if (x, y) != (0, 0) and not self.grid[y][x].has_pit:
                self.grid[y][x].has_gold = True
                break

    def place_wumpus(self):
        while True:
            x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            if (x, y) != (0, 0) and not self.grid[y][x].has_pit and not self.grid[y][x].has_gold:
                self.grid[y][x].has_wumpus = True
                break

    def place_player(self):
        self.grid[0][0].has_player = True
        self.grid[0][0].visited_by_player = True
        self.grid[0][0].visible_to_agent = True 

    def print_grid(self):
        for row in self.grid:
            print(' '.join(str(tile) for tile in row)) '''
    
# During the test simulation run, I removed this to make it cleaner, more modular(reusable), 
# also to make unit testing easier aage ke liye.
# Now, I can Reset the world mid-simulation
# Generate multiple variations to try out shit
# do not have to put manual placements in main.py anymore. Weeeeee
