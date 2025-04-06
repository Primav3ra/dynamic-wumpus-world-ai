from .base_agent import BaseAgent
from collections import deque
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

