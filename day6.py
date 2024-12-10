from io import StringIO, TextIOBase

exem = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

class Labyrinthe:
    labi:list[list[bool]]
    
    seen:list[list[bool]]
    
    pos_i:int
    pos_j:int
    dir_i:int
    dir_j:int

    height:int
    width:int

    SYMB_TO_DIR = {
        "^": (-1, 0),
        ">": (0, 1),
        "<": (0, -1),
        "v": (1, 0),
    }

    TURN = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0)
    }

    def __init__(self, src:TextIOBase) -> None:
        lines: list[str] = list(src)
        self.height = len(lines)
        self.width = len(lines[0])

        self.labi = [
            [lines[i][j] == "#" for j in range(self.width)] for i in range(self.height)
        ]

        self.seen = [[False for j in range(self.width)] for i in range(self.height)] 

        for i in range(self.height):
            for j in range(self.width):
                if lines[i][j] in self.SYMB_TO_DIR:
                    self.dir_i, self.dir_j = self.SYMB_TO_DIR[lines[i][j]]
                    self.pos_i = i
                    self.pos_j = j
                    self.seen[i][j] = True

    def __repr__(self) -> str:
        return f"Labyrinthe({self.labi}, {self.pos_i}, {self.pos_j})"
    
    def __str__(self) -> str:
        to_char = {
             (False, False) : ".",
             (True, False) : "#",
             (False, True): "*"
         }
        return "\n".join(
            "".join( to_char[self.labi[i][j], self.seen[i][j]]
                    for j in range(self.width)
            )
            for i in range(self.height)
        )
    
    def nb_seen(self) -> int:
        c = 0
        for line in self.seen:
            for s in line:
                if s:
                    c += 1
    
        return c
    
    def step(self) -> bool:
        ni = self.pos_i + self.dir_i
        nj = self.pos_j + self.dir_j
        if ni < 0 or ni >= self.height:
            return False
        if nj < 0 or nj >= self.width:
            return False
        if self.labi[ni][nj]:
            self.dir_i, self.dir_j = self.TURN[(self.dir_i, self.dir_j)]
        else:
            self.pos_i = ni
            self.pos_j = nj
        return True

    def parcours(self) -> int:
        while self.step():
            self.seen[self.pos_i][self.pos_j] = True
        
        return self.nb_seen()

lb_exem = Labyrinthe(StringIO(exem))
print(lb_exem)
lb_exem.step()
print(lb_exem)
lb_exem = Labyrinthe(StringIO(exem))
print(lb_exem.parcours())
print(lb_exem)

import urllib.request

PB_FILE_NAME = "input-06-1.txt"
# urllib.request.urlretrieve("https://adventofcode.com/2024/day/6/input", PB_FILE_NAME)

with open(PB_FILE_NAME) as f:
    lb = Labyrinthe(f)
    print(lb.parcours())

