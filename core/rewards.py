def update_scores(self, player, wumpus):
    if player.has_gold:
        self.player_score += 100
    if player.has_exited:
        self.player_score += 50
    if player.is_dead:
        self.player_score -= 100
        self.wumpus_score += 100

    # Exploration Reward
    if player.just_moved:
        self.player_score += 1

    # Wumpus Movement Intelligence (e.g., moved closer)
    if hasattr(wumpus, 'moved_closer') and wumpus.moved_closer:
        self.wumpus_score += 3
    elif hasattr(wumpus, 'moved_closer') and not wumpus.moved_closer:
        self.wumpus_score -= 5

    # Player escapes (e.g., moved away from Wumpus)
    if hasattr(player, 'escaped') and player.escaped:
        self.player_score += 5
        self.wumpus_score -= 3
