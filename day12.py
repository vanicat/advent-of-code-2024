from collections.abc import Iterator
from contextlib import contextmanager
from typing import Optional, cast
from grid import D, Grid, V

class Region():
    inside: set[V]

    size: V

    symbol: str
    area: int
    perimeter: int

    _min: Optional[V]
    _max: Optional[V]
    _sides: Optional[int]

    def __init__(self, height: int, width: int, symbol:str) -> None:
        self.symbol = symbol
        self.area = 0
        self.perimeter = 0

        self._min = V(height, width)
        self._max = V(0, 0)

        self.size = V(height, width)
        self.inside = set()


    def __contains__(self, pos: V):
        return pos in self.inside

    
    def __setitem__(self, pos: V, value:bool) -> None:
        if (pos in self.inside) == value:
            return

        if value:
            self.inside.add(pos)

            if self._min is not None:
                if pos.i < self._min.i:
                    self._min = self._min.copy(i=pos.i)
                if pos.j < self._min.j:
                    self._min = self._min.copy(j=pos.j)

            if self._max is not None:
                if pos.i > self._max.i:
                    self._max = self._max.copy(i=pos.i)
                if pos.j > self._max.j:
                    self._max = self._max.copy(j=pos.j)
            
            self._sides = None

            self.area += 1
            for dir in D.ALL_DIR:
                if pos + dir in self:
                    self.perimeter -= 1
                else:
                    self.perimeter += 1
        else:
            self._min = None
            self._max = None
            self._sides = None

            self.inside.remove(pos)

            self.area -= 1
            for dir in D.ALL_DIR:
                if pos + dir in self:
                    self.perimeter += 1
                else:
                    self.perimeter -= 1


    def __iter__(self) -> Iterator[V]:
        for i in range(self.min.i, self.max.i + 1):
            for j in range(self.min.j, self.max.j + 1):
                if V(i, j) in self.inside:
                    yield V(i, j)


    def find_min_max(self):
        min = self.size
        max = V(0, 0)
        for pos in self.inside:
            if pos.i < min.i:
                min = min.copy(i=pos.i)
            if pos.j < min.j:
                min = min.copy(j=pos.j)
            if pos.i > max.i:
                max = max.copy(i=pos.i)
            if pos.j > max.j:
                max = max.copy(j=pos.j)

        self._min = min
        self._max = max



    @property
    def min(self) -> V: 
        if self._min is None:
            self.find_min_max()
        
        assert self._min is not None
        return self._min

    @property
    def max(self) -> V:
        if self._max is None:
            self.find_min_max()
        
        assert self._max is not None
        return self._max
        
    @property
    def sides(self) -> int:
        if self._sides is not None:
            return self._sides
        
        return self.find_sides()
    
    def find_sides(self) -> int:
        horiz = self.find_horiz_sides()

        vert = self.find_vert_sides()

        self._sides = horiz + vert
        return self._sides

    def find_vert_sides(self) -> int:
        vert = 0

        for j in range(self.min.j, self.max.j + 2):
            left = False
            right = False
            for i in range(self.min.i, self.max.i + 1):
                pos_right = V(i, j)
                pos_left = V(i, j-1)

                if (not left or right) and (pos_left in self) and (pos_right not in self):
                    vert += 1

                if (left or not right) and (pos_left not in self) and (pos_right in self):
                    vert += 1

                left = pos_left in self
                right = pos_right in self
        return vert

    def find_horiz_sides(self) -> int:
        horiz = 0

        for i in range(self.min.i, self.max.i + 2):
            up = False
            down = False
            for j in range(self.min.j, self.max.j + 1):
                pos = V(i, j)
                pos_up = V(i-1, j)

                if (not down or up) and (pos in self) and (pos_up not in self):
                    horiz += 1

                if (down or not up) and (pos not in self) and (pos_up in self):
                    horiz += 1

                down = pos in self
                up = pos_up in self

        return horiz

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                self.symbol if V(i, j) in self else "." for j in range(self.min.j, self.max.j + 1)
            ) for i in range(self.min.i, self.max.i + 1)
        )

class Day12:
    grid: Grid[str]

    _regions: Optional[list[Region]]
    seen: Optional[Grid[bool]]

    def __init__(self, data:str) -> None:
        parsed_data = [line.strip() for line in data.strip().split("\n")]

        self.grid = Grid(len(parsed_data), len(parsed_data[0]), lambda i, j: parsed_data[i][j])
        self._regions = None
        self.seen = None
    
    def find_region(self, pos:V) -> Region:
        assert self.seen is not None

        symbol = self.grid[pos]
        result = Region(self.grid.size.i, self.grid.size.j, symbol)

        stack:list[V] = [pos]
        result[pos] = True
        self.seen[pos] = True

        while stack:
            pos = stack.pop()
            for dir in D.ALL_DIR:
                n_pos = pos + dir
                if n_pos in self.grid and self.grid[n_pos] == symbol and not self.seen[n_pos]:
                    stack.append(n_pos)
                    result[n_pos] = True
                    self.seen[n_pos] = True


        return result
    
    @contextmanager
    def explore(self):
        self.seen = Grid(self.grid.size.i, self.grid.size.j, False)
        try:
            yield
        finally:
            self.seen = None


    def _find_all_region(self):
        with self.explore():
            assert self.seen is not None
            self._regions = []
            for pos in self.grid.iter_pos():
                if not self.seen[pos]:
                    region = self.find_region(pos)
                    self._regions.append(region)

    @property
    def regions(self) -> list[Region]:
        if self._regions is None:
            self._find_all_region()
        return cast(list[Region], self._regions)

    def cost(self):
        return sum(r.area * r.perimeter for r in self.regions)
    
    def cost_discount(self):
        return sum(
            r.area * r.sides
            for r in self.regions
        )


if __name__ == "__main__":
    EXEM = """AAAA
BBCD
BBCC
EEEC
""" 
    areas = {
        "A": 4, "B": 4, "C": 4, "E": 3, "D": 1
    }
    perimeter = {
        "A": 10, "B": 8, "C": 10, "E": 8, "D": 4
    }
    exem1_pb = Day12(EXEM)
    for region in exem1_pb.regions:
        assert region.area == areas[region.symbol]
        assert region.perimeter == perimeter[region.symbol]

    EXEM2 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""" 
    areas = {
        "A": 4, "B": 4, "C": 4, "E": 3, "D": 1
    }
    perimeter = {
        "A": 10, "B": 8, "C": 10, "E": 8, "D": 4
    }
    exem2_pb = Day12(EXEM2)

    for region in exem2_pb.regions:
        if region.symbol == "X":
            assert region.area == 1
            assert region.perimeter == 4
        else:
            assert region.area == 21
            assert region.perimeter == 36
    
    EXEM3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
    exem3_pb = Day12(EXEM3)
    assert len(exem3_pb.regions) == 11
    for region in exem3_pb.regions:
        if region.symbol == "R":
            assert region.area == 12
            assert region.perimeter == 18
        elif region.symbol == "F":
            assert region.area == 10
            assert region.perimeter == 18
    assert exem3_pb.cost() == 1930

    with open("input-12-1.txt") as f:
        data = f.read()
    
    pb = Day12(data)
    print("Day 12 cost 1 is", pb.cost())

    for region, side in zip(exem1_pb.regions, [4, 4, 8, 4, 4]):
        assert region.find_sides() == side

    assert exem1_pb.cost_discount() == 80
    assert exem2_pb.cost_discount() == 436

    exem4_pb = Day12("""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""")

    for region, side in zip(exem4_pb.regions, [12, 4, 4]):
        assert region.find_sides() == side

    assert exem4_pb.cost_discount() == 236

    print("Day 12 cost discount is", pb.cost_discount())