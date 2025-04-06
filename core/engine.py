class GameEngine:
    def __init__(self, grid, player, wumpus, max_turns=100):
        self.grid = grid
        self.player = player
        self.wumpus = wumpus
        self.max_turns = max_turns
        self.turn = 0
        self.game_over = False

    def next_turn(self):
        if self.game_over or self.turn >= self.max_turns:
            print("Game Over: Max turns reached or someone died.")
            return

        self.turn += 1
        print(f"\n--- TURN {self.turn} ---")
        print(f"\n===== TURN {self.turn} =====")
        print(f"Player is at ({self.player.x}, {self.player.y})")
        print(f"Wumpus is at ({self.wumpus.x}, {self.wumpus.y})")

        # Show grid state before actions
        self.grid.print_grid(self.player, self.wumpus)

        # 1. Player makes a move (user or RL agent)
        self.player.take_turn(self.grid)

        # 2. Check if game ended after player move
        if self.player.is_dead or self.player.has_exited:
            self.game_over = True
            return

        # 3. Wumpus makes a move (AI agent)
        self.wumpus.take_turn(self.grid, self.player)

        # 4. Check if player got caught
        if self.player.x == self.wumpus.x and self.player.y == self.wumpus.y:
            print("The Wumpus has caught the Player!")
            self.player.is_dead = True
            self.game_over = True

        # 5. Update perceptions
        self.grid.update_perceptions()

        # 6. Score update
        self.grid.rewards.update_scores(self.player, self.wumpus)

        # Show updated grid after actions
        self.grid.print_grid(self.player, self.wumpus)

        # Show scores
        if hasattr(self.grid, 'rewards'):
             self.grid.rewards.print_scores(self.turn)

