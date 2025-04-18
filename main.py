import argparse
from core.game import start_game

def parse_arguments():
    parser = argparse.ArgumentParser(description="Dynamic Wumpus World AI")
    parser.add_argument(
        '--manual',
        action='store_true',
        help='Enable manual mode for user-controlled player.'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    manual_mode = args.manual
    print(f"[DEBUG] Player manual_mode set to {manual_mode}")

    start_game()













#This was a test Run for phase 1 before I started developing the core
'''

def run_dry_simulation():
    print("\n--- DRY RUN START ---\n")

    # 1. Create grid and manually place things for control
    grid = Grid(size=4)
    player = Player("Player", x=0, y=0)
    wumpus = Wumpus("Wumpus", x=2, y=1)  # You can randomize this later if needed

    grid.grid[player.y][player.x].has_player = True
    grid.grid[wumpus.y][wumpus.x].has_wumpus = True  # Optional — AI Wumpus may move to this

    #VISUALIZATION
    grid.print_grid() 

    # 4. Print perceptions
    player_perception = grid.get_perception(player.x, player.y, is_player=True)
    player.perceive(player_perception)

    wumpus_perception = grid.get_perception(wumpus.x, wumpus.y, is_player=False)
    wumpus.perceive(wumpus_perception)

    print("\n--- DRY RUN END ---\n")

if __name__ == "__main__":
    run_dry_simulation()

'''

