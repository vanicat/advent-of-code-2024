from heapq import heappop, heappush
from typing import cast
from grid import Grid, V, D




def dijkstra(start:V, end:V, grid:Grid[bool]):
    done:Grid[bool] = Grid(grid.size.i, grid.size.j, lambda i, j: False)
    dists:Grid[int] = Grid(grid.size.i, grid.size.j, cast(int, float("inf")))
    origins:Grid[list[V]] = Grid(grid.size.i, grid.size.j, lambda i,j: list())

    priority_queue:list[tuple[int, V]] = [(0, start)]

    while priority_queue != []:
        dist, location = heappop(priority_queue)

        if done[location]:
            continue

        done[location] = True

        ndir: D
        ndist = dist + 1
        for ndir in D.ALL_DIR:
            npos = location + ndir
            if npos not in grid or done[npos] or dists[npos] < ndist or grid[npos]:
                continue

            if dists[npos] == ndist:
                origins[npos].append(location)
            else:
                dists[npos] = ndist
                origins[npos] = [location]

                heappush(priority_queue, (ndist, npos))


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

def do_it(data:str, height:int, width:int):
    grid = Grid(height+1, width+1, False, lambda b: "#" if b else ".")
    for i, line in enumerate(data.strip().split("\n")):
        if i >= 1024:
            break
        x, y = line.strip().split(",")
        x = int(x)
        y = int(y)
        grid[V(y, x)] = True
    
    dists, origin = dijkstra(V(0, 0), V(height, width), grid)
    print(dists[V(height, width)])
    # print(display_grid(start, end, grid, dists, origin))
    # print(score_grid(start, end, grid, dists, origin))

if __name__ == "__main__":
    with open("input-18-1.txt") as f:
        do_it(f.read(), 70, 70)
    
