from dataclasses import dataclass
from functools import total_ordering
from heapq import heappop, heappush


def decompact(entry:str) -> list[int|None]:
    result:list[int|None] = []
    file:bool = True
    id = 0
    for nb in entry:
        nb = int(nb)
        if file:
            result.extend(id for i in range(nb))
            id = id + 1
        else:
            result.extend(None for i in range(nb))

        file = not file

    return result


def read_disk(disk) -> list[int|None]:
    return [None if c == "." else int(c) for c in disk]


def defrag(disk:list[int|None]) -> None:
    i = 0
    j = len(disk) - 1
    while i < j:
        while disk[i] is not None:
            i = i + 1
        while disk[j] is None:
            j = j - 1
        if i >= j:
            return
        disk[i] = disk[j]
        disk[j] = None
        i = i + 1
        j = j - 1


def checksum(disk:list[int|None]) -> int:
    result = 0
    for i, id in enumerate(disk):
        if id is not None:
            result += id*i
    
    return result

@dataclass
@total_ordering
class Block():
    id: int
    length: int
    pos: int

    def __lt__(self, other:"Block|Empty"):
        return (self.pos, self.length) < (other.pos, other.length)

@dataclass
@total_ordering
class Empty():
    length: int
    pos: int
    valid: bool = True

    def __lt__(self, other:"Block|Empty"):
        return (self.pos, self.length) < (other.pos, other.length)


class Multi_heap():
    heaps: list[list[Empty]]

    def __init__(self) -> None:
        self.heaps = [[] for _ in range(10)]

    def push(self, elem:Empty) -> None:
        for i in range(0, elem.length + 1):
            heappush(self.heaps[i], elem)

    def pop(self, length:int) -> Empty|None:
        heap = self.heaps[length]

        while heap:
            elem = heappop(heap)
            if elem.valid:
                elem.valid = False
                return elem
            
        return None


def defrag2(entry:str) -> int:
    emptys_block: Multi_heap = Multi_heap()
    blocks:list[Block] = []
    file:bool = True
    id = 0
    pos = 0
    for c in entry:
        length = int(c)
        if file:
            blocks.append(Block(id, length, pos))
            id = id + 1
        else:
            new_empt = Empty(length, pos)
            emptys_block.push(new_empt)
        pos += length
        file = not file
    
    for block in reversed(blocks):
        may_be_pos = emptys_block.pop(block.length)
        if may_be_pos is not None:
            block.pos = may_be_pos.pos
            if may_be_pos.length > block.length:
                emptys_block.push(Empty(may_be_pos.length - block.length, may_be_pos.pos + block.length))

    checksum = 0

    for block in blocks:
        for i in range(block.pos, block.pos + block.length):
            checksum += i * block.id

    return checksum






if __name__ == "__main__":
    exem = "2333133121414131402"
    exem_disk = decompact(exem)
    assert exem_disk == read_disk("00...111...2...333.44.5555.6666.777.888899")
    defrag(exem_disk)
    assert exem_disk == read_disk("0099811188827773336446555566..............")
    assert checksum(exem_disk) == 1928
    assert defrag2(exem) == 2858

    # https://adventofcode.com/2024/day/9/input as "input-09-1.txt"

    with open("input-09-1.txt") as f:
        pb = f.read().strip()
        disk = decompact(pb)
        defrag(disk)
        print(checksum(disk))
        print(defrag2(pb))