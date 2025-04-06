
class Perception:
    def __init__(self, stench=False, breeze=False, glitter=False, bump=False, scream=False, sees_player=False):
        self.stench = stench
        self.breeze = breeze
        self.glitter = glitter
        self.bump = bump
        self.scream = scream
        self.sees_player = sees_player

    def as_list(self):
        return [
            "Stench" if self.stench else None,
            "Breeze" if self.breeze else None,
            "Glitter" if self.glitter else None,
            "Bump" if self.bump else None,
            "Scream" if self.scream else None,
            "See_Player" if self.sees_player else None,
        ]
