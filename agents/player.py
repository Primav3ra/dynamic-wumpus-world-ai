
from agents.base_agent import BaseAgent
import random
import math

class Player(BaseAgent):
    def __init__(self, name, x=0, y=0, manual_mode=False):
        print(f"[DEBUG] Player manual_mode set to {manual_mode}")
        super().__init__(name, x, y)
        self.manual_mode=manual_mode
        self.has_gold = False
        self.has_exited = False
        self.escaped = False
        self.just_moved = False
        self.is_dead = False

    def take_turn(self, grid):
        self.just_moved = False
        self.escaped = False

        # Find valid moves
        moves = grid.get_valid_moves(self.x, self.y)
        if not moves:
            print("Player is stuck!")
            return
        
        if self.manual_mode:
            print("\n🕹️ Manual Mode: Choose your move.")
            print(f"Valid moves from ({self.x}, {self.y}): {moves}")
            print("Use WASD keys to move (W=up, S=down, A=left, D=right)")

        key_map = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        move = None
        while move is None:
            key = input("Your move (W/A/S/D or Q to Quit): ").lower()
            if key == 'q':
                print("👋 Goodbye, adventurer.")
                exit()
            if key in key_map:
                dx, dy = key_map[key]
                new_pos = (self.x + dx, self.y + dy)
                if new_pos in moves:
                    move = new_pos
                else:
                    print("❌ Invalid move. That tile is not allowed.")
            else:
                print("❌ Invalid key. Use W/A/S/D only.")
        else:
            move = random.choice(moves) # Choose a move randomly (replace with RL policy if needed)
        
        old_distance = self._distance_to_wumpus(grid)

        self.x, self.y = move
        self.just_moved = True

        new_distance = self._distance_to_wumpus(grid)
        if new_distance > old_distance:
            self.escaped = True

        current_tile = grid.get_tile(self.x, self.y)

        if current_tile.has_pit:
            print("Player fell into a pit!")
            self.is_dead = True
        elif current_tile.has_wumpus:
            print("Player walked into the Wumpus!")
            self.is_dead = True
        elif current_tile.has_gold:
            print("Player found gold!")
            self.has_gold = True
            current_tile.has_gold = False
        elif current_tile.is_exit and self.has_gold:
            print("Player exited the world with gold!")
            self.has_exited = True
        elif current_tile.is_exit and self.has_gold:
            self.has_exited = True
            print("🚪 Player has exited the cave with the gold!")

    def _distance_to_wumpus(self, grid):
        if not hasattr(grid, 'wumpus'):
            return float('inf')
        wx, wy = grid.wumpus.x, grid.wumpus.y
        return math.hypot(self.x - wx, self.y - wy)
    

#BEFORE THE MAJOR CHANGES TO REWARD SYSTEM
'''
from .base_agent import BaseAgent

class Player(BaseAgent):
    def __init__(self, name, x=0, y=0):
        super().__init__(name, x, y)
        self.has_arrow = True

    def perceive(self, perception):
        print(f"[Player] Perception at ({self.x}, {self.y}): {perception.as_list()}")
        self.record_memory(perception)

# PHASE 2 - For now: manual user input or later: RL policy 

    def take_turn(self, grid):
        print(f"Perceptions: {self.perceive(grid)}")
        action = input("Choose action [F=Forward, L=Left, R=Right, G=Grab, S=Shoot, Q=Quit]: ").upper()
        self.act(action, grid) 
'''

