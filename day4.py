#%% l'exemple

exem:list[str] = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".split() # type: ignore

#%% pb1

WORD = "XMAS"

def is_fixmas(txt:list[str], x0:int, y0:int, vx:int, vy:int) -> bool:
    x, y = x0, y0
    for i in range(4):
        if y < 0 or y >= len(txt) or x < 0 or x >= len(txt[y]) or txt[y][x] != WORD[i]:
            return False
        x += vx
        y += vy
    return True

assert is_fixmas(exem, 5, 0, 1, 0)
assert is_fixmas(exem, 4, 1, -1, 0)
assert is_fixmas(exem, 5, 9, 1, -1)
assert not is_fixmas(exem, 5, 0, 0, 1)
assert not is_fixmas(exem, 5, 0, 0, -1)
assert not is_fixmas(exem, 5, 0, 1, 1)
assert not is_fixmas(exem, 5, 0, 1, -1)

DIR = [(vx, vy) for vx in (-1, 0, 1) for vy in (-1, 0, 1) if vx != 0 or vy != 0]

def count_xmas(txt:list[str]):
    count = 0
    for y in range(len(txt)):
        for x in range(len(txt[y])):
            for vx, vy in DIR:
                if is_fixmas(txt, x, y, vx, vy):
                    count += 1
    
    return count

assert count_xmas(exem) == 18

#%% resol pb

with open("input-04-1.txt") as f:
    pb = list(f)

print("pb1:", count_xmas(pb))

#%% pb2

MAS = "MAS"

CROSSDIR = [(vx, vy) for vx in (-1, 1) for vy in (-1, 1)]


def is_mas(txt:list[str], x0:int, y0:int, vx:int, vy:int) -> bool:
    return txt[y0-vy][x0-vx] == MAS[0] and txt[y0+vy][x0+vx] == MAS[2]
    

assert is_mas(exem, 2, 1, 1, 1)
assert is_mas(exem, 2, 1, 1, -1)
assert not is_mas(exem, 2, 1, -1, 1)
assert not is_mas(exem, 2, 1, -1, -1)

def near_x_y(txt:list[str], x, y):
    return "\n".join([line[x-1:x+2] for line in txt[y-1:y+2]])

def count_x_mas(txt:list[str]):
    count:int = 0
    for y in range(1, len(txt) - 1):
        for x in range(1, len(txt[y]) - 1):
            if txt[y][x] == "A":
                half_x_mas:bool = False

                for vx, vy in CROSSDIR:
                    if is_mas(txt, x, y, vx, vy):
                        if half_x_mas:
                            count += 1
                            print(near_x_y(txt, x, y), "\n")
                        else:
                            half_x_mas = True
        
    return count

assert count_x_mas(exem) == 9

# %%

#%% resol pb

with open("input-04-1.txt") as f:
    pb = list(f)

print("pb2 :", count_x_mas(pb))
# %%
