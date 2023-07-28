import sys
import math
from pathlib import Path


def input_echo():
    s = input()
    print(s, file=sys.stderr, flush=True)
    return s


def read_from(f):
    scenario_file = open(Path(__file__).parent / "data" / "scenario.txt", "r")

    def wrapper():
        return scenario_file.readline().rstrip("\n")

    return wrapper


@read_from
def input_from_file():
    pass


class Pac:
    def __init__(self):
        tokens = INPUT_METHOD().split()
        self.pac_id = int(tokens[0])  # unique within a team
        self.is_mine = tokens[1] != "0"  # True if this pac is yours
        self.x = int(tokens[2])
        self.y = int(tokens[3])
        self.type_id = tokens[4]  # "ROCK", "PAPER", "SCISSORS"
        self.speed_turns_left = int(tokens[5])
        self.ability_cooldown = int(tokens[6])


class Map:
    def __init__(self):
        self.width, self.height = [int(i) for i in INPUT_METHOD().split()]
        self.cells = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.my_pacs = []
        self.opp_pacs = []
        for y in range(self.height):
            for x, ch in enumerate(INPUT_METHOD()):
                self.cells[x][y] = 0 if ch == " " else -1

    def update(self):
        # reset and read pacs
        self.my_pacs = []
        self.opp_pacs = []
        n_visible_pacs = int(INPUT_METHOD())
        for i in range(n_visible_pacs):
            if (pac := Pac()).is_mine:
                self.my_pacs.append(pac)
            else:
                self.opp_pacs.append(pac)
        # reset and update pellets
        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y] > 0:
                    self.cells[x][y] = 0
        n_visible_pellets = int(INPUT_METHOD())
        for i in range(n_visible_pellets):
            x, y, value = [int(j) for j in INPUT_METHOD().split()]
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


# INPUT_METHOD = input
# INPUT_METHOD = input_echo
INPUT_METHOD = input_from_file


map = Map()
while True:
    my_score, opponent_score = [int(i) for i in INPUT_METHOD().split()]
    map.update()

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
