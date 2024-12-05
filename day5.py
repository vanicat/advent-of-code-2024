#%%
# Part One
 
from io import StringIO, TextIOBase
from typing import TypedDict

exem = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

def exem_io() -> StringIO:
    return StringIO(exem)

class Problem(TypedDict):
    before: dict[int, list[int]]
    after: dict[int, list[int]]
    updates: list[list[int]]


def read_pb(input:TextIOBase) -> Problem:
    before:dict[int, list[int]] = {}
    after:dict[int, list[int]] = {}

    for line in input:
        line = line.strip()
        if line == "":
            break
        i = line.find("|")
        fst = line[:i]
        snd = line[i+1:]
        before.setdefault(int(snd), []).append(int(fst))
        after.setdefault(int(fst), []).append(int(snd))
        
    printing = [[int(x) for x in line.strip().split(",")] for line in input]

    return {
         "before": before, 
         "after" : after,
         "updates": printing
    }

exem_pb = read_pb(exem_io())
# %%
def good_update(update: list[int], pb:Problem) -> bool:
    seen = set()
    for x in update:
        for y in pb["after"].get(x, []):
            if y in seen:
                return False
        seen.add(x)
    return True

assert good_update(exem_pb["updates"][0], exem_pb)
assert good_update(exem_pb["updates"][1], exem_pb)
assert good_update(exem_pb["updates"][2], exem_pb)
   
assert not good_update(exem_pb["updates"][3], exem_pb)
assert not good_update(exem_pb["updates"][4], exem_pb)
assert not good_update(exem_pb["updates"][5], exem_pb)
# %%
def updates_values(pb:Problem) -> int:
    c = 0
    for update in pb["updates"]:
        if good_update(update, pb):
            c += update[len(update) // 2]
    return c

assert updates_values(exem_pb) == 143
# %%
with open("input-05-1.txt") as f:
    print(updates_values(read_pb(f)))
# %%

# Part Two

def correct(update:list[int], pb:Problem):
    result:list[int] = []
    befores:dict[int, set[int]] = {}
    elems:set[int] = set(update)
    
    for v in update:
        before_v = set()
        for pred in pb["before"].get(v, []):
            if pred in elems:
                before_v.add(pred)
        befores[v] = before_v

    
    while befores:
        available = set()
        for v, before in befores.items():
            if not before:
                available.add(v)
        for v in available:
            del befores[v]
            result.append(v)
            for before in befores.values():
                before.discard(v)
            
    return result


assert correct(exem_pb["updates"][3], exem_pb) == [97, 75, 47, 61, 53]
assert correct(exem_pb["updates"][4], exem_pb) == [61, 29, 13]
assert correct(exem_pb["updates"][5], exem_pb) == [97, 75, 47, 29, 13]

#%%

def incorrect_updates_values(pb:Problem) -> int:
    c = 0
    for update in pb["updates"]:
        if not good_update(update, pb):
            update = correct(update, pb)
            c += update[len(update) // 2]
    return c

assert incorrect_updates_values(exem_pb) == 123

# %%

with open("input-05-1.txt") as f:
    print(incorrect_updates_values(read_pb(f)))


# %%
