from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Optional


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

    def copy(self, *, i:Optional[int]=None, j:Optional[int]=None) -> "V":
        if i is None:
            i = self.i
        if j is None:
            j = self.j
        return V(i, j)

class D(V):
    ALL_DIR: ClassVar[list["D"]] = []
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
    
    @classmethod
    def all_dir(cls):
        yield D(-1, 0)
        yield D(0, 1)
        yield D(1, 0)
        yield D(0, -1)


pred = D(0, -1)
for letter, dir in [("^", D(-1, 0)), (">", D(0, 1)), ("v", D(1, 0)), ("<", D(0, -1))]:
    D.SYMB_TO_DIR[letter] = dir
    D.DIR_TO_SYMB[dir] = letter
    D.TURN[pred] = dir
    D.ALL_DIR.append(dir)
    pred = dir

# TURN:dict[V, V] = {
#     V(-1, 0): V(0, 1),
#     V(0, 1): V(1, 0),
#     V(1, 0): V(0, -1),
#     V(0, -1): V(-1, 0)
# }


class Grid[T]:
    labi:dict[V, T]

    size:V

    str_elem: Callable[[T], str]

    def __init__(self, height:int, width:int, default:Optional[T | Callable[[int, int], T]] = None, str_elem:Optional[Callable[[T], str]] = None) -> None:
        self.size = V(height, width)

        self.labi = {} 

        if str_elem is not None:
            self.str_elem = str_elem
        else:
            self.str_elem = str

        if default is None:
            return
        
        for i in range(self.size.i):
            for j in range(self.size.j):
                pos = V(i, j)

                if isinstance(default, Callable):
                    self.labi[pos] = default(i, j)
                else:
                    self.labi[pos] = default


    def __contains__(self, pos:V):
        return 0 <= pos.i < self.size.i and 0 <= pos.j < self.size.j

    def __repr__(self) -> str:
        return f"Labyrinthe({self.labi}"
    
    def to_str(self, str_elem: Callable[[T], str]) -> str:
        return "\n".join("".join(str_elem(self[V(i, j)]) for j in range(self.size.j)) for i in range(self.size.i))
    
    def __str__(self) -> str:
        if self.str_elem is None:
            return self.__repr__()
        else:
            return self.to_str(self.str_elem)
    
    def __getitem__(self, pos:V) -> T:
        return self.labi[pos]
        
    def __setitem__(self, pos:V, value:T) -> None:
        self.labi[pos] = value
    
    def __iter__(self) -> Generator[T]:
        for i in range(self.size.i):
            for j in range(self.size.j):
                yield self.labi[V(i, j)]
    
    def iter_pos(self) -> Generator[V]:
        for i in range(self.size.i):
            for j in range(self.size.j):
                yield V(i, j)

    def items(self) -> Generator[tuple[V, T]]:
        for i in range(self.size.i):
            for j in range(self.size.j):
                pos = V(i, j)
                yield pos, self.labi[pos]
    
