class RewardSystem:
    def __init__(self):
        self.player_score = 0
        self.wumpus_score = 0

    def update_scores(self, player, wumpus):
        # Base survival reward per turn
        if not player.is_dead and not player.has_exited:
            self.player_score += 1  # Surviving each turn earns something

        # Check player status
        if player.has_gold:
            self.player_score += 10
            print("[REWARD] Player has collected gold! (+10)")

        if player.is_dead:
            self.player_score -= 50
            self.wumpus_score += 20
            print("[PENALTY] Player died! (-50)")
            print("[REWARD] Wumpus caused death! (+20)")

        if player.has_exited:
            self.player_score += 50
            print("[REWARD] Player exited safely! (+50)")

        # Wumpus scoring based on strategy (track smarter movement)
        if (wumpus.x, wumpus.y) == (player.x, player.y):
            self.wumpus_score += 50
            self.player_score -= 50
            print("[REWARD] Wumpus caught the Player! (+50 Wumpus)")

        # Reward Wumpus for actively reducing distance (simple heuristic)
        prev_distance = self.manhattan_distance(wumpus.prev_position, (player.x, player.y)) \
            if hasattr(wumpus, 'prev_position') else None
        curr_distance = self.manhattan_distance((wumpus.x, wumpus.y), (player.x, player.y))

        if prev_distance and curr_distance < prev_distance:
            self.wumpus_score += 2
            print("[REWARD] Wumpus got closer to Player. (+2)")

        # Track Wumpus last position for next round
        wumpus.prev_position = (wumpus.x, wumpus.y)

        self.display_scores()

    def display_scores(self):
        print(f"🎯 Scores => Player: {self.player_score} | Wumpus: {self.wumpus_score}")

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
