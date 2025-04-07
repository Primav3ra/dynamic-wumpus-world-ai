
import random
from env.tile import Tile
from .perception import Perception

GRID_SIZE = 8
PIT_PROBABILITY = 0.15

class Grid:
    def __init__(self, size=8):
        self.size = size
        self.grid = [[Tile(x, y) for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
        self.generate_world()
        self.width = self.size
        self.height = self.size


    def generate_world(self, num_pits=5, num_wumpus=1):
       from agents.player import Player
       from agents.wumpus import Wumpus

       all_coords = [(x, y) for x in range(self.size) for y in range(self.size) if (x, y) != (0, 0)]
       random.shuffle(all_coords)

    # 1. Place Player at (0,0)
       self.player = Player(name="Player", x=0, y=0)

    # 2. Place Wumpus
       w_x, w_y = all_coords.pop()
       self.grid[w_y][w_x].has_wumpus = True
       self.wumpus = Wumpus(name="Wumpus", x=w_x, y=w_y)

    # 3. Place Gold
       gold_x, gold_y = all_coords.pop()
       self.grid[gold_y][gold_x].has_gold = True

    # 4. Place Pits
       for _ in range(num_pits):
           pit_x, pit_y = all_coords.pop()
           self.grid[pit_y][pit_x].has_pit = True
    
    # creating an exit tile - [7][7]
       self.grid[7][7].is_exit = True

#for grid coordinates that will be used by wumpus to find player:

    def get_adjacent_coords(self, x, y):
        width = len(self.grid[0]) #width
        length = len(self.grid) #length
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        adjacent = []

        for dx, dy in directions:
           new_x, new_y = x + dx, y + dy
           if 0 <= new_x < self.width and 0 <= new_y < self.height:
               adjacent.append((new_x, new_y))

           return adjacent


    def print_grid(self, player=None, wumpus=None):
       print("\nWumpus World:")
       print("+" + "----+" * self.size)
       for y in range(self.size):
         row = "|"
         for x in range(self.size):
            tile = self.grid[y][x]

            if player and player.x == x and player.y == y:
                char = "🧍"   # Player
            elif wumpus and wumpus.x == x and wumpus.y == y:
                char = "👹"   # Wumpus
            elif tile.has_gold:
                char = "💰"   # Gold
            elif tile.has_pit:
                char = "🕳️"   # Pit
            else:
                char = "⬜"   # Empty tile

            row += f" {char} |"
         print(row)
         print("+" + "----+" * self.size)


#returns a list of valid tile positions the player can move to - PHASE 3
    
    def get_valid_moves(self, x, y):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if not self.grid[ny][nx].has_pit:
                    moves.append((nx, ny))

        print(f"Valid moves from ({x},{y}): {moves}")
        return moves
    
 #this is for player.py in take_turn() 
   
    def get_tile(self, x, y):
       if 0 <= x < self.size and 0 <= y < self.size:
           return self.grid[y][x]
       return None


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
    
    def update_perceptions(self):
        for y in range(self.size):
            for x in range(self.size):
               p = self.get_perception(x, y)
               tile = self.grid[y][x]
               tile.has_stench = p.stench
               tile.has_breeze = p.breeze
               tile.has_glitter = p.glitter


#experimental 
'''
    def print_full_grid(self):
       print("\nWumpus World (Full View):")
       for y in range(self.size):
        row = ""
        for x in range(self.size):
            cell = self.grid[y][x]
            if cell.has_player:
                row += " 🧍 "
            elif cell.has_wumpus:
                row += " 👹 "
            elif cell.has_gold:
                row += " 💰 "
            elif cell.has_pit:
                row += " 🕳️ "
            else:
                row += " . "
        print(row)
'''


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
