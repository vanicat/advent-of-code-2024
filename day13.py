from collections.abc import Iterator
from dataclasses import dataclass
import math
from typing import Optional
from grid import V

len_button = len("Button A: ")
len_prize = len("Prize: ")

def gcd(a:int, b:int) -> tuple[int, int, int]:
    
    u = 1
    v = 0
    x = 0
    y = 1

    while b > 0:
        r = a % b
        q = a // b

        x, u = u - q * x, x
        y, v = v - q * y, y

        a = b
        b = r
    
    return (a, u, v)

def eqn_soluce(a:int, b:int, res:int) -> Iterator[tuple[int, int]]:
    diviseur, λa, λb = gcd(a, b)

    if res % diviseur != 0:
        return
    
    da, db, q = a // diviseur, b // diviseur, res // diviseur

    ca, cb = q * λa, q * λb

    q = ca // db 
    ca -= q * db
    cb += q * da

    assert ca >= 0
        
    while cb >= 0:
        yield (ca, cb)
        ca += db
        cb -= da


def det(a:V, b:V) -> int:
    return a.i * b.j - a.j * b.i

@dataclass
class Claw:
    button_a: V
    button_b: V

    prize: V

    def __init__(self, data:str) -> None:
        a, b, p = (line.strip() for line in data.strip().split("\n"))

        def read_line(line:str, len_start:int) -> V:
            stx, sty = line[len_start:].split(", ")
            stx = stx[2:]
            sty = sty[2:]
            return V(int(stx), int(sty))

        self.button_a = read_line(a, len_button)
        self.button_b = read_line(b, len_button)
        self.prize = read_line(p, len_prize)

    def __str__(self) -> str:
        return f"""\
Button A: X+{self.button_a.i}, Y+{self.button_a.j}
Button B: X+{self.button_b.i}, Y+{self.button_b.j}
Prize: X={self.prize.i}, Y={self.prize.j}
"""
    
    def test_soluce_y(self, na: int, nb:int):
        return na * self.button_a.j + nb * self.button_b.j == self.prize.j

    def smallest_cost(self) -> Optional[int]:
        sol = self.solve_both_eqn()
        if sol is not None:
            na, nb = sol
            return 3 * na + nb
    
        return None
    
    def solve_both_eqn(self) -> Optional[tuple[int, int]]:
        d  = det(self.button_a, self.button_b)
        db = det(self.button_a, self.prize)
        da = det(self.prize, self.button_b)
        na = da // d
        nb = db // d

        if na * self.button_a + nb * self.button_b == self.prize:
            return (na, nb)
        

    @staticmethod
    def reads(data:str) -> Iterator["Claw"]:
        for claw_data in data.split("\n\n"):
            yield Claw(claw_data)

def part_two_transform(claw:Claw) -> Claw:
    claw.prize = claw.prize + (10000000000000, 10000000000000)
    return claw

def total_cost(data:Iterator[Claw]) -> int:
    total = 0
    for claw in data:
        if (cost := claw.smallest_cost()) is not None:
            total += cost
            print(total, cost)
    return total

def test_eqn_soluce(a, b, r):
    found = False
    for ca, cb in eqn_soluce(a, b, r):
        found = True
        # print(f"{ca} * {a} + {cb} * {b} == {r}")
        assert ca * a + cb * b == r
        assert ca > 0
        assert cb > 0
    assert found



if __name__ == "__main__":
    claw1 = Claw("""
        Button A: X+94, Y+34
        Button B: X+22, Y+67
        Prize: X=8400, Y=5400
    """)
    assert claw1.button_a == V(94, 34)
    assert claw1.button_b == V(22, 67)
    assert claw1.prize == V(8400, 5400)

    (q, ca, cb) = gcd(94, 34)
    assert q == 94 * ca + 34 * cb

    test_eqn_soluce(94, 22, 8400)
    test_eqn_soluce(34, 67, 5400)

    assert det(V(1, 0), V(0, 1)) == 1
    assert det(V(3, 4), V(5, 9)) == 3 * 9 - 4 * 5

    assert claw1.smallest_cost() == 280

    claw1.solve_both_eqn()

    EXEM = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

    for claw, res in zip(Claw.reads(EXEM), [280, None, 200, None]):
        assert claw.smallest_cost() == res

    assert total_cost(Claw.reads(EXEM)) == 480

    with open("input-13-1.txt") as f:
        print("cost pb 1:", total_cost(Claw.reads(f.read())))

    with open("input-13-1.txt") as f:
        print("cost pb 2:", total_cost((part_two_transform(claw) for claw in Claw.reads(f.read()))))