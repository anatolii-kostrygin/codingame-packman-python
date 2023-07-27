import sys
import math


class Pac:
    def __init__(self, read_f):
        inputs = read_f().split()
        self.pac_id = int(inputs[0])  # pac number (unique within a team)
        self.is_mine = inputs[1] != "0"  # true if this pac is yours
        self.x = int(inputs[2])  # position in the grid
        self.y = int(inputs[3])  # position in the grid
        self.type_id = inputs[4]  # unused in wood leagues
        self.speed_turns_left = int(inputs[5])  # unused in wood leagues
        self.ability_cooldown = int(inputs[6])  # unused in wood leagues


class Map:
    def __init__(self, read_f):
        self.width, self.height = [int(i) for i in read_f().split()]
        self.cells = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.my_pacs = []
        self.opp_pacs = []
        for y in range(self.height):
            for x, ch in enumerate(read_f()):
                self.cells[x][y] = 0 if ch == " " else -1

    def update(self, read_f):
        # reset and read pacs
        self.my_pacs = []
        self.opp_pacs = []
        n_visible_pacs = int(read_f())  # all your pacs and enemy pacs in sight
        for i in range(n_visible_pacs):
            pac = Pac(read_f)
            if pac.is_mine:
                self.my_pacs.append(pac)
            else:
                self.opp_pacs.append(pac)
        # reset and update pellets
        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y] > 0:
                    self.cells[x][y] = 0
        n_visible_pellets = int(read_f())
        for i in range(n_visible_pellets):
            x, y, value = [int(j) for j in read_f().split()]
            self.cells[x][y] = value

    def find_closest_target(self, pac_x, pac_y, min_pellets):
        best_target = None
        best_dist = 100500
        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y] >= min_pellets:
                    d = m_dist(x, y, pac_x, pac_y)
                    if d < best_dist:
                        best_target = x, y
        return best_target


def m_dist(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


map = Map(input)
# game loop
while True:
    my_score, opponent_score = [int(i) for i in input().split()]
    map.update(input)

    commands = []
    for pac in map.my_pacs:
        if (target := map.find_closest_target(pac.x, pac.y, 2)) is not None:
            commands.append(f"MOVE {pac.pac_id} {target[0]} {target[1]}")
        elif (target := map.find_closest_target(pac.x, pac.y, 1)) is not None:
            commands.append(f"MOVE {pac.pac_id} {target[0]} {target[1]}")
        else:
            print(f"Could not find target for pac_id={pac.pac_id} at ({pac.x}, {pac.y})", file=sys.stderr, flush=True)
    if commands:
        print(" | ".join(commands))
    else:
        print("MOVE 0 15 10")

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
