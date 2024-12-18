from typing import Callable
from grid import Grid, V, D

class Topo_map(Grid[int]):
    start_pos: list[V]

    def __init__(self, data:str) -> None:
        lines:list[str] = [striped_line for line in data.split("\n") if (striped_line:=line.strip()) != ""]

        def set_height(i:int, j:int) -> int:
            return int(lines[i][j])
        
        grid_height = len(lines)
        grid_width = len(lines[0])

        super().__init__(grid_height, grid_width, default=set_height)

        self.start_pos = []

        for pos, height in self.items():
            if height == 0:
                self.start_pos.append(pos)

    def find_trails(self, pos:V) -> dict[V, int]:
        current_pos = {pos:1}
        for height in range(1, 10):
            next_pos = {}
            for pos,nb in current_pos.items():
                for dir in D.ALL_DIR:
                    n_pos = pos + dir
                    if n_pos in self and self[n_pos] == height:
                        next_pos[n_pos] = next_pos.get(n_pos, 0) + nb
            if next_pos == {}:
                return {}
            current_pos = next_pos

        return current_pos
    
    def first_score(self) -> int:
        return sum(len(self.find_trails(pos)) for pos in self.start_pos)
    
    def snd_score(self) -> int:
        return sum(sum(self.find_trails(pos).values()) for pos in self.start_pos)
    
    

    

if __name__ == "__main__":
    exemple = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    exemple_map = Topo_map(exemple)
    for start, value in zip(exemple_map.start_pos, [5, 6, 5, 3, 1, 3, 5, 3, 5]):
        assert len(exemple_map.find_trails(start)) == value, f"incorrect value for start {start}"
    assert exemple_map.first_score() == 36, f"incorrect exemple score pb 1"

    for start, value in zip(exemple_map.start_pos, [20, 24, 10, 4, 1, 4, 5, 8, 5]):
        assert sum(exemple_map.find_trails(start).values()) == value, f"incorrect value for start {start}"
    assert exemple_map.snd_score() == 81, f"incorrect exemple score pb 2"


    with open("input-10-1.txt") as f:
        map = Topo_map(f.read())
        print("first problem score", map.first_score())
        print("snd problem score", map.snd_score())