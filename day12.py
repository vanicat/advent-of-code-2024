from contextlib import contextmanager
from typing import Callable, Optional
from grid import D, Grid, V

class Region(Grid[bool]):
    symbol: str
    area: int
    perimeter: int

    def __init__(self, height: int, width: int, symbol:str) -> None:
        self.symbol = symbol
        self.area = 0
        self.perimeter = 0

        super().__init__(height, width, False, lambda b: self.symbol if b else ".")

    def __contains__(self, pos: V):
        return pos in self.labi and self[pos]
    
    def __setitem__(self, pos: V, value:bool) -> None:
        if self.labi[pos] == value:
            return
        
        self.labi[pos] = value
        if value:
            self.area += 1
            for dir in D.ALL_DIR:
                if pos + dir in self:
                    self.perimeter -= 1
                else:
                    self.perimeter += 1
        else:
            self.area -= 1
            for dir in D.ALL_DIR:
                if pos + dir in self:
                    self.perimeter += 1
                else:
                    self.perimeter -= 1

    def first_pos(self) -> V:
        for pos in self.iter_pos():
            if pos in self:
                return pos
        raise ValueError("no first pos on empty region")        
            
    


class Day12:
    grid: Grid[str]

    regions: list[Region]
    seen: Optional[Grid[bool]]

    def __init__(self, data:str) -> None:
        parsed_data = [line.strip() for line in data.strip().split("\n")]

        self.grid = Grid(len(parsed_data), len(parsed_data[0]), lambda i, j: parsed_data[i][j])
        self.regions = []
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


    def find_all_region(self):
        with self.explore():
            assert self.seen is not None
            for pos in self.grid.iter_pos():
                if not self.seen[pos]:
                    region = self.find_region(pos)
                    self.regions.append(region)

    def cost(self):
        return sum(r.area * r.perimeter for r in self.regions)


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
    exem_pb = Day12(EXEM)
    exem_pb.find_all_region()
    for region in exem_pb.regions:
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
    exem_pb = Day12(EXEM2)
    exem_pb.find_all_region()

    for region in exem_pb.regions:
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
    exem_pb = Day12(EXEM3)
    exem_pb.find_all_region()
    assert len(exem_pb.regions) == 11
    for region in exem_pb.regions:
        if region.symbol == "R":
            assert region.area == 12
            assert region.perimeter == 18
        elif region.symbol == "F":
            assert region.area == 10
            assert region.perimeter == 18
    assert exem_pb.cost() == 1930

    with open("input-12-1.txt") as f:
        data = f.read()
    
    pb = Day12(data)
    pb.find_all_region()
    print("Day 12 cost 1 is", pb.cost())
