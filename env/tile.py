
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.has_pit = False
        self.has_gold = False
        self.has_wumpus = False
        self.has_player = False
        self.is_exit = False

        self.visited_by_player = False
        self.visible_to_agent = False

    def is_safe_to_enter(self):
        return not self.has_wumpus and not self.has_pit
    
    def __repr__(self):
        items = []
        if self.has_pit: items.append("P")
        if self.has_gold: items.append("G")
        if self.has_wumpus: items.append("W")
        if self.has_player: items.append("A")
        return f"[{''.join(items) or ' '}]"
