from collections.abc import Callable
from heapq import heappop, heappush
from typing import cast
from grid import D, V, Grid

exem = """
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

def read(data) -> tuple[V, V, Grid[bool]]:
    start: V
    end: V 
    
    def wall_builder(i:int, j:int) -> bool:
        return True
    def other_builder(i:int, j:int) -> bool:
        return False
    def start_builder(i:int, j:int) -> bool:
        nonlocal start
        start = V(i, j)
        return False
    def end_builder(i:int, j:int) -> bool:
        nonlocal end
        end = V(i, j)
        return False

    selector:dict[str, Callable[[int, int], bool]] = {
        "#": wall_builder,
        ".": other_builder,
        "S": start_builder,
        "E": end_builder
    }

    grid:Grid[bool] = Grid.from_str(data, selector, str_elem=lambda x:"#" if x else ".")

    return start, end, grid

def init_dist(*args) -> dict[D, int]:
    return {
        d: cast(int, float("inf")) for d in D.ALL_DIR
    }


def init_origin(*args) -> dict[D, list[tuple[V, D]]]:
    return {
        d: [] for d in D.ALL_DIR
    }


def dijkstra(start:V, end:V, grid:Grid[bool]):
    done:Grid[set[D]] = Grid(grid.size.i, grid.size.j, lambda i, j: set())
    dists:Grid[dict[D, int]] = Grid(grid.size.i, grid.size.j, init_dist)
    origins:Grid[dict[D, list[tuple[V, D]]]] = Grid(grid.size.i, grid.size.j, init_origin)

    priority_queue:list[tuple[int, V, D]] = [(0, start, D.from_str(">"))]

    while priority_queue != []:
        dist, location, direction = heappop(priority_queue)

        if direction in done[location]:
            continue

        done[location].add(direction)

        npos: V
        ndir: D
        ndist: int
        for npos, ndir, ndist in [
            (location + direction, direction, dist + 1),
            (location, direction.turn_right(), dist + 1000),
            (location, direction.turn_left(), dist + 1000)
        ]:
            if ndir in done[npos] or dists[npos][ndir] < ndist or grid[npos]:
                continue

            if dists[npos][ndir] == ndist:
                origins[npos][ndir].append((location, direction))
            else:
                dists[npos][ndir] = ndist
                origins[npos][ndir] = [(location, direction)]

                heappush(priority_queue, (ndist, npos, ndir))


    return dists, origins

def display_grid(start:V, end:V, grid:Grid[bool], dists:Grid[dict[D, int]], origin:Grid[dict[D, list[tuple[V, D]]]]):
    disp_grid:Grid[str] = Grid(grid.size.i, grid.size.j, ".")

    for loc in disp_grid.iter_pos():
        if grid[loc]:
            disp_grid[loc] = "#"

    to_see:list[tuple[V, D]] = []
    min_dist = float("inf")
    for dir, dist in dists[end].items():
        if dist < min_dist:
            to_see = [(end, dir)]
            min_dist = dist
        if dist == min_dist:
            to_see.append((end, dir))
    
    while to_see:
        pos, dir = to_see.pop()
        if disp_grid[pos] == ".":
            disp_grid[pos] = str(dir)
        elif disp_grid[pos] != str(dir):
            disp_grid[pos] = '+'

        for (npos, ndir) in origin[pos][dir]:
            if (npos, ndir) not in to_see:
                to_see.append((npos, ndir))


    return disp_grid

def score_grid(start:V, end:V, grid:Grid[bool], dists:Grid[dict[D, int]], origin:Grid[dict[D, list[tuple[V, D]]]]):
    seen_grid:Grid[set[D]] = Grid(grid.size.i, grid.size.j, lambda i, j: set())

    to_see:list[tuple[V, D]] = []
    min_dist:int = cast(int, float("inf"))
    for dir, dist in dists[end].items():
        if dist < min_dist:
            to_see = [(end, dir)]
            min_dist = dist
        if dist == min_dist:
            to_see.append((end, dir))

    score1:int = min_dist
    score2:int = 0
    
    while to_see:
        pos, dir = to_see.pop()
        if dir in seen_grid[pos]:
           continue

        if not seen_grid[pos]:
            score2 += 1
        seen_grid[pos].add(dir) 

        for (npos, ndir) in origin[pos][dir]:
            to_see.append((npos, ndir))


    return score1, score2

def do_it(data):
    start, end, grid = read(data)
    dists, origin = dijkstra(start, end, grid)
    print(display_grid(start, end, grid, dists, origin))
    print(score_grid(start, end, grid, dists, origin))

if __name__ == "__main__":
    do_it(exem)
    do_it("""
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""")
    with open("input-16-1.txt") as f:
        do_it(f.read())
    
