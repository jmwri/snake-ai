class DeathReason:
    def __init__(self, reason: str):
        self.reason = reason


ILLEGAL_BACKWARDS = DeathReason("Tried to move backwards")
ILLEGAL_TOO_FAR = DeathReason("Tried to move > 1 tile away")
ILLEGAL_DIAGONAL = DeathReason("Tried to move diagonally")
HIT_SNAKE = DeathReason("Hit snake")
HIT_WALL = DeathReason("Hit wall")
