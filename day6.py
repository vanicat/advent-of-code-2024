from dataclasses import dataclass
from io import StringIO, TextIOBase
from typing import ClassVar

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

@dataclass(slots=True, frozen=True)
class V:
    i: int
    j: int
    
    def __str__(self):
        return f"({self.i}, {self.j})"
    
    def __add__(self, other:"V|Iterable|Any") -> "V":
        if isinstance(other, V):
            return V(self.i + other.i, self.j + other.j)
        else:
            try:
                i, j = other
                return V(self.i + i, self.j + j)
            except TypeError|ValueError:
                raise NotImplemented
    
    def __sub__(self, other:"V|Iterable|Any") -> "V":
        if isinstance(other, V):
            return V(self.i - other.i, self.j - other.j)
        else:
            try:
                i, j = other
                return V(self.i - i, self.j - j)
            except TypeError|ValueError:
                raise NotImplemented
            
    def __rmult__(self, other):
        if isinstance(other, int):
            return V(self.i * other, self.j * other)
        raise NotImplemented
    
    def __iter__(self):
        yield self.i
        yield self.j


class D(V):
    SYMB_TO_DIR: ClassVar[dict[str, "D"]] = {}
    DIR_TO_SYMB: ClassVar[dict["D", str]] = {}
    TURN: ClassVar[dict["D", "D"]] = {}

    @classmethod
    def from_str(cls, st:str) -> "D":
        return D.SYMB_TO_DIR[st]
    
    def __str__(self) -> str:
        return D.DIR_TO_SYMB[self]
    
    def turn(self) -> "D":
        return D.TURN[self]


pred = D(0, -1)
for k, v in [("^", D(-1, 0)), (">", D(0, 1)), ("v", D(1, 0)), ("<", D(0, -1))]:
    D.SYMB_TO_DIR[k] = v
    D.DIR_TO_SYMB[v] = k
    D.TURN[pred] = v
    pred = v

# TURN:dict[V, V] = {
#     V(-1, 0): V(0, 1),
#     V(0, 1): V(1, 0),
#     V(1, 0): V(0, -1),
#     V(0, -1): V(-1, 0)
# }


class Dir_manager:
    line_dir: dict[D, list[bool]]

    def __init__(self, size:V):
        self.line_dir = {}

        for dir in D.DIR_TO_SYMB:
            if dir.i == 0:
                self.line_dir[dir] = [False for j in range(size.j)]
            else:
                self.line_dir[dir] = [False for i in range(size.i)]


    def add_dir(self, pos:V, dir:D):
        if dir.i == 0:
            self.line_dir[dir][pos.i] = True
        else:
            self.line_dir[dir][pos.j] = True


    def check_dir(self, pos:V, dir:D):
        if dir.i == 0:
            return self.line_dir[dir][pos.i]
        else:
            return self.line_dir[dir][pos.j]


class Labyrinthe:
    labi:dict[V, bool]
    
    seen:dict[V, set[D]]

    line_dir: Dir_manager
    
    pos:V
    dir:D

    size:V


    def __init__(self, src:TextIOBase) -> None:
        lines: list[str] = [l.strip() for l in list(src)]

        self.size = V(len(lines), len(lines[0]))

        self.labi = {} 

        self.seen = {}

        self.line_dir = Dir_manager(self.size)

        for i in range(self.size.i):
            for j in range(self.size.j):
                pos = V(i, j)

                self.labi[pos] = lines[i][j] == "#"
                self.seen[pos] = set()

                if lines[i][j] in D.SYMB_TO_DIR:
                    self.dir = D.from_str(lines[i][j])
                    self.pos = pos
                    self.seen[pos].add(self.dir)

    def __contains__(self, pos:V):
        return 0 <= pos.i < self.size.i and 0 <= pos.j < self.size.j

    def __repr__(self) -> str:
        return f"Labyrinthe({self.labi}, {self.pos.i}, {self.pos.j})"
    
    def __str__(self) -> str:
        def yield_chars(i):
            for j in range(self.size.j):
                if self.labi[V(i, j)]:
                    yield "#"
                elif not self.seen[V(i, j)]:
                    yield "."
                elif len(self.seen[V(i, j)]) != 1:
                    yield "*"
                else:
                    fst, = self.seen[V(i, j)]
                    yield str(fst)

        return "\n".join("".join(yield_chars(i)) for i in range(self.size.i))
    
    def nb_seen(self) -> int:
        c = 0
        for s in self.seen.values():
            if s:
                c += 1
    
        return c
    
    def step(self) -> bool:
        n_pos = self.pos + self.dir

        if not n_pos in self:
            return False
        elif self.labi[n_pos]:
            self.dir = self.dir.turn()
            # return self.step()
        else:
            self.pos = n_pos
        return True

    def parcours(self) -> int:
        while self.step():
            self.seen[self.pos].add(self.dir)
        return self.nb_seen()

    def check_line(self, dir:V) -> bool:
        pos = self.pos
        while pos in self:
            if self.labi[pos]:
                return False
            if dir in self.seen[pos]:
                return True
            pos += dir
        return False
        
    def parcours2(self) -> int:
        nb = 0
        while self.step():
            if self.line_dir.check_dir(self.pos, self.dir.turn()):
                if self.check_line(self.dir.turn()):
                    #print(f"could turn at ({self.pos})")
                    nb += 1
            self.seen[self.pos].add(self.dir)
            self.line_dir.add_dir(self.pos, self.dir)

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

from typing import Any, ClassVar, Iterable, Self, Sequence
import urllib.request

PB_FILE_NAME = "input-06-1.txt"
# urllib.request.urlretrieve("https://adventofcode.com/2024/day/6/input", PB_FILE_NAME)

with open(PB_FILE_NAME) as f:
    lb = Labyrinthe(f)
    print("parcours 1:", lb.parcours())


with open(PB_FILE_NAME) as f:
    lb = Labyrinthe(f)
    print("parcours 2:", lb.parcours2())


