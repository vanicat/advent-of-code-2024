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
    
    seen:list[list[set[tuple[int, int]]]]
    
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

    DIR_TO_SYMB = {
        (-1, 0): "^",
        (0,  1): ">",
        (0, -1): "<",
        (1,  0): "v",
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

        self.seen = [[set() for j in range(self.width)] for i in range(self.height)] 

        for i in range(self.height):
            for j in range(self.width):
                if lines[i][j] in self.SYMB_TO_DIR:
                    self.dir_i, self.dir_j = self.SYMB_TO_DIR[lines[i][j]]
                    self.pos_i = i
                    self.pos_j = j
                    self.seen[i][j].add((self.dir_i, self.dir_j))

    def __repr__(self) -> str:
        return f"Labyrinthe({self.labi}, {self.pos_i}, {self.pos_j})"
    
    def __str__(self) -> str:
        to_char = {
             (False, False) : ".",
             (True, False) : "#",
             (False, True): "*"
        }
        def yield_chars(i):
            for j in range(self.width):
                if self.labi[i][j]:
                    yield "#"
                elif not self.seen[i][j]:
                    yield "."
                elif len(self.seen[i][j]) != 1:
                    yield "*"
                else:
                    elem:set = self.seen[i][j]
                    yield self.DIR_TO_SYMB[next(iter(self.seen[i][j]))]

        return "\n".join("".join(yield_chars(i)) for i in range(self.height))
    
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
        elif nj < 0 or nj >= self.width:
            return False
        elif self.labi[ni][nj]:
            self.dir_i, self.dir_j = self.TURN[(self.dir_i, self.dir_j)]
            # return self.step()
        else:
            self.pos_i = ni
            self.pos_j = nj
        return True

    def parcours(self) -> int:
        while self.step():
            self.seen[self.pos_i][self.pos_j].add((self.dir_i, self.dir_j))
        return self.nb_seen()

        
    def parcours2(self) -> int:
        while self.step():
            if self.TURN[(self.dir_i, self.dir_j)] in self.seen[self.pos_i][self.pos_j]:
                print(f"cycle found at ({self.pos_i}, {self.pos_j})")
            self.seen[self.pos_i][self.pos_j].add((self.dir_i, self.dir_j))
            print(self)

        return self.nb_seen()


lb_exem = Labyrinthe(StringIO(exem))
print(lb_exem)
lb_exem.step()
print(lb_exem)
lb_exem = Labyrinthe(StringIO(exem))
print(lb_exem.parcours())
print(lb_exem)

lb_exem = Labyrinthe(StringIO(exem))
print(lb_exem.parcours2())
print(lb_exem)

import urllib.request

PB_FILE_NAME = "input-06-1.txt"
# urllib.request.urlretrieve("https://adventofcode.com/2024/day/6/input", PB_FILE_NAME)

with open(PB_FILE_NAME) as f:
    lb = Labyrinthe(f)
    print(lb.parcours())


