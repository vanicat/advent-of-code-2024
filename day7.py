#%% import

from io import StringIO, TextIOBase

#%% exemple
exemple:str = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

# %% reading

type pb_type = list[tuple[int, list[int]]]

def read_lines(input:TextIOBase) -> pb_type:
    sep1 = [line.strip().split(": ") for line in input]
    return [(int(value), [int(x) for x in ops.split(" ")]) for value, ops in sep1]

pb_exem = read_lines(StringIO(exemple))
assert pb_exem == [(190, [10, 19]), (3267, [81, 40, 27]), (83, [17, 5]), (156, [15, 6]), (7290, [6, 8, 6, 15]), (161011, [16, 10, 13]), (192, [17, 8, 14]), (21037, [9, 7, 18, 13]), (292, [11, 6, 16, 20])]

# %%

def try_line(value:int, ops:list[int]) -> bool:
    def try_line_rec(value:int, ops:list[int], i:int) -> bool:
        if i == 0:
            return value == ops[0]
        
        v = ops[i]

        if value % v == 0 and try_line_rec(value // v, ops, i - 1):
            return True
        
        if value >= v and try_line_rec(value - v, ops, i - 1):
            return True
        
        return False
    return try_line_rec(value, ops, len(ops) - 1)

for i in range(len(pb_exem)):
    if i in [0, 1, 8]:
        assert try_line(*pb_exem[i]), f"{pb_exem[i]} n'est pas trouvé"
    else:
        assert not try_line(*pb_exem[i]), f"{pb_exem[i]} n'est pas trouvé"

# %%

def total_calibration_result(pb:pb_type) -> int:
    return sum((value for value, ops in pb if try_line(value, ops)))

assert total_calibration_result(pb_exem) == 3749
# %% the pb1

# get input from https://adventofcode.com/2024/day/7/input

with open("input-07-1.txt") as f:
    the_problem = read_lines(f)

print(total_calibration_result(the_problem))


# %%

def try_line2(value:int, ops:list[int]) -> bool:
    def try_line_rec(value:int, ops:list[int], i:int) -> bool:
        if i == 0:
            return value == ops[0]
        
        v = ops[i]

        lenv = 1
        while lenv <= v:
            lenv = lenv * 10

        if value % lenv == v and try_line_rec(value // lenv, ops, i - 1):
            act.append("//")
            return True

        if value % v == 0 and try_line_rec(value // v, ops, i - 1):
            act.append("*")
            return True
        
        if value >= v and try_line_rec(value - v, ops, i - 1):
            act.append("+")
            return True
        
        return False
    
    act = []

    return try_line_rec(value, ops, len(ops) - 1)

for i in range(len(pb_exem)):
    if i in [0, 1, 3, 4, 6, 8]:
        assert try_line2(*pb_exem[i]), f"{pb_exem[i]} n'est pas trouvé"
    else:
        assert not try_line2(*pb_exem[i]), f"{pb_exem[i]} n'est pas trouvé"

assert try_line2(1110, [1, 1, 10])
# %%

def total_calibration_result2(pb:pb_type) -> int:
    return sum((value for value, ops in pb if try_line2(value, ops)))

assert total_calibration_result2(pb_exem) == 11387
# %%

with open("input-07-1.txt") as f:
    the_problem = read_lines(f)

print(total_calibration_result2(the_problem))
# %%

# some test

# %%
