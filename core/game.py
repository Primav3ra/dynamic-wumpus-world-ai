from env.grid import Grid
from agents.player import Player
from agents.wumpus import Wumpus
from core.engine import GameEngine
from core.rewards import RewardSystem

def start_game(grid_size=6, max_turns=30, num_pits=5, num_wumpus=1):
    print("🔥 Simulation starting...")
    grid = Grid(size=grid_size)
    grid.generate_world(num_pits=num_pits, num_wumpus=num_wumpus)

    player = grid.player
    wumpus = grid.wumpus

    grid.rewards = RewardSystem()

    engine = GameEngine(grid, player, wumpus, max_turns=max_turns)

    while not engine.game_over:
        print("Running next turn...")
        engine.next_turn()





'''def start_game(grid_size=6, max_turns=30, num_pits=5, num_wumpus=1):
    print("🔥 Simulation starting...")
    # 1. Create the grid
    grid = Grid(size=grid_size)
    grid.generate_world(num_pits=num_pits, num_wumpus=num_wumpus)

    # 2. Grab player and wumpus placed during world generation
    player = grid.player
    wumpus = grid.wumpus

    # 3. Attach reward system
    grid.rewards = RewardSystem()

    # 4. Initialize and run engine
    engine = GameEngine(grid, player, wumpus, max_turns=max_turns)

    while not engine.game_over:
        engine.next_turn()'''

