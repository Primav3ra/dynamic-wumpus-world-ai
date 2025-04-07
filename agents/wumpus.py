from .base_agent import BaseAgent
import random
from collections import deque

class Wumpus:
    def __init__(self, x, y, name="Wumpus"):
        self.x = x
        self.y = y
        self.reward = 0

    def take_turn(self, grid, player):
        current_distance = abs(self.x - player.x) + abs(self.y - player.y)
        next_move = self.plan_move_towards(player, grid)

        if not next_move:
              print("Wumpus sees no path. Patrolling randomly.")
              possible_moves = grid.get_valid_moves(self.x, self.y)
              if possible_moves:
                   next_move = random.choice(possible_moves)
                   self.move(next_move, grid)
              return
            # Patrol randomly
            
        possible_moves = grid.get_valid_moves(self.x, self.y)
        if possible_moves:
            next_move = random.choice(possible_moves)

        if next_move:
            moved = self.move(next_move, grid)
            if moved:
                new_distance = abs(self.x - player.x) + abs(self.y - player.y)
                if new_distance < current_distance:
                    self.reward += 1
                elif new_distance > current_distance:
                    self.reward -= 1
                print(f"🎯 Wumpus Reward: {self.reward}")

    def plan_move_towards(self, player, grid):
        path = self.bfs_to_player(grid, player)
        if path and len(path) > 1:
            return path[1]  # next move (not current position)
        return None

    def bfs_to_player(self, grid, player):
        start = (self.x, self.y)
        goal = (player.x, player.y)
        visited = set()
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            current = path[-1]

            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in grid.get_adjacent_coords(*current):
                tile = grid.grid[neighbor[1]][neighbor[0]]
                if not tile.has_pit:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def move(self, position, grid):
        new_x, new_y = position
        if 0 <= new_x < grid.size and 0 <= new_y < grid.size:
            # Clear old tile
            grid.grid[self.y][self.x].has_wumpus = False

            # Update position
            self.x = new_x
            self.y = new_y

            # Set new tile
            grid.grid[self.y][self.x].has_wumpus = True
            return True
        return False









#SOME ERROR IDK
'''from collections import deque
import random

class Wumpus(BaseAgent):
    def __init__(self, name, x=0, y=0):
        super().__init__(name, x, y)
        self.memory = set()  # For tracking visited/safe tiles later
        self.just_moved = False
        self.is_alive = True  # Optional, for future extensibility

    def perceive(self, perception):
        print(f"[Wumpus] Perception at ({self.x}, {self.y}): {perception.as_list()}")
        self.record_memory(perception)

    # === PHASE 2: WUMPUS AI ===
    def take_turn(self, grid, player):
        self.just_moved = False  # Reset before moving

        next_move = self.plan_move_towards(player, grid)
        self.prev_position = (self.x, self.y)

        if next_move:
            moved = self.move(next_move, grid)
            self.just_moved = moved  # Used by rewards.py
        else:
            print(f"{self.name} waits. No path to player.")

    def plan_move_towards(self, player, grid):
        # BFS pathfinding to locate the shortest path to the player
        path = self.bfs_to_player(grid, player)
        if path and len(path) > 1:
            return self.direction_to(path[0])  # Convert coord to movement direction
        return None

    def bfs_to_player(self, grid, player):
        start = (self.x, self.y)
        goal = (player.x, player.y)
        queue = deque([(start, [])])
        visited = set()

        while queue:
            (current, path) = queue.popleft()
            if current == goal:
                return path

            for neighbor in grid.get_adjacent_coords(*current):
                if neighbor in visited:
                    continue
                tile = grid.get_tile(*neighbor)
                if tile and not tile.has_pit:  # Avoid pits
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return []

    def direction_to(self, target_coord):
        dx = target_coord[0] - self.x
        dy = target_coord[1] - self.y

        if dx == 1: return 'RIGHT'
        if dx == -1: return 'LEFT'
        if dy == 1: return 'DOWN'
        if dy == -1: return 'UP'
        return None
'''
