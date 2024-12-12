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

type vec = tuple[int, int]


class Dir_manager:
    line_dir: dict[vec, list[bool]]

    def __init__(self, height:int, width:int):
        self.line_dir = {}

        for dir in Labyrinthe.DIR_TO_SYMB:
            if dir[0] == 0:
                self.line_dir[dir] = [False for j in range(width)]
            else:
                self.line_dir[dir] = [False for i in range(height)]

    def add_dir(self, i:int, j:int, dir_i:int, dir_j:int):
        if dir_i == 0:
            self.line_dir[(dir_i, dir_j)][i] = True
        else:
            self.line_dir[(dir_i, dir_j)][j] = True

    def check_dir(self, i:int, j:int, dir_i:int, dir_j:int):
        if dir_i == 0:
            return self.line_dir[(dir_i, dir_j)][i]
        else:
            return self.line_dir[(dir_i, dir_j)][j]


class Labyrinthe:
    labi:list[list[bool]]
    
    seen:list[list[set[vec]]]

    line_dir: Dir_manager
    
    pos_i:int
    pos_j:int
    dir_i:int
    dir_j:int

    height:int
    width:int

    SYMB_TO_DIR:dict[str, vec] = {
        "^": (-1, 0),
        ">": (0, 1),
        "<": (0, -1),
        "v": (1, 0),
    }

    DIR_TO_SYMB:dict[vec, str] = {
        (-1, 0): "^",
        (0,  1): ">",
        (0, -1): "<",
        (1,  0): "v",
    }

    TURN:dict[vec, vec] = {
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

        self.line_dir = Dir_manager(self.height, self.width)

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

    def check_line(self, dir_i, dir_j) -> bool:
        i = self.pos_i
        j = self.pos_j
        while 0 <= i < self.height and 0 <= j < self.width:
            if self.labi[i][j]:
                return False
            if (dir_i, dir_j) in self.seen[i][j]:
                return True
            i += dir_i
            j += dir_j
        return False
        
    def parcours2(self) -> int:
        nb = 0
        while self.step():
            if self.line_dir.check_dir(self.pos_i, self.pos_j, *self.TURN[self.dir_i, self.dir_j]):
                if self.check_line(*self.TURN[self.dir_i, self.dir_j]):
                    print(f"could turn at ({self.pos_i, self.pos_j})")
                    nb += 1
            self.seen[self.pos_i][self.pos_j].add((self.dir_i, self.dir_j))
            self.line_dir.add_dir(self.pos_i, self.pos_j, self.dir_i, self.dir_j)

        return nb


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


with open(PB_FILE_NAME) as f:
    lb = Labyrinthe(f)
    print(lb.parcours2())


