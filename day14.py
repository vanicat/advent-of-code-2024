import math
from typing import Iterable
from grid import V

import arcade #(using arcade 3.0.0-dev.40)


class Robot:
    pos: V
    speed: V

    size: V

    def __init__(self, size:V, data:str) -> None:
        self.size = size

        p_data, v_data = data.split(" ")
        p_j, p_i = (int(x) for x in p_data[2:].split(","))
        v_j, v_i = (int(x) for x in v_data[2:].split(","))

        self.pos = V(p_i, p_j)
        self.speed = V(v_i, v_j)

    def advance(self, n:int) -> V:
        n_pos = self.pos + n * self.speed
        return self.normalize(n_pos)

    def normalize(self, n_pos):
        return V(n_pos.i % self.size.i, n_pos.j % self.size.j)
    
    def step(self, n:int=1) -> None:
        n_pos = self.pos + n * self.speed
        self.pos = self.normalize(n_pos)
    
    def rev_step(self, n:int=1) -> None:
        n_pos = self.pos - n * self.speed
        self.pos = self.normalize(n_pos)
    
def read_robots(height:int, width:int, data:str):
    size = V(height, width)
    return [Robot(size, line.strip()) for line in data.strip().split("\n")]
    
def count_by_cadran(size, where:Iterable[V]) -> tuple[int, int, int, int]:
    mid_i = size.i // 2
    mid_j = size.j // 2
    c11 = 0
    c21 = 0
    c12 = 0
    c22 = 0
    for pos in where:
        if mid_i < pos.i and mid_j < pos.j:
            c11 += 1
        if mid_i < pos.i and mid_j > pos.j:
            c12 += 1
        if mid_i > pos.i and mid_j < pos.j:
            c21 += 1
        if mid_i > pos.i and mid_j > pos.j:
            c22 += 1
    
    return c11, c21, c12, c22
        
def pb1(data:str) -> int:
    robots = read_robots(103, 101, data)
    cadrants = count_by_cadran(V(103, 101), (r.advance(100) for r in robots))
    return math.prod(cadrants)

class MyView(arcade.View):
    def __init__(self, height, width, data) -> None:
        super().__init__()

        self.robots = read_robots(height, width, data)
        self.time = 0
        self.step = False
        self.rev_step = False
        self.pause = True

        self.nb = 0
        self.nb_disp = arcade.Text("count:              ", self.width // 2 - 200, 10)

        self.speed = 101
        self.adv_robots(14)

    def on_update(self, delta_time: float) -> None:
        if self.pause and not self.step and not self.rev_step:
            return
        
        if self.rev_step:
            self.rev_step = False

            self.adv_robots(-1)
            
        self.time += delta_time
        if self.time > 0.25 or self.step:
            self.time = self.time % 0.25

            self.step = False

            self.adv_robots(self.speed)

    def adv_robots(self, n:int):
        self.nb += n
        for r in self.robots:
            r.step(n)


    def on_draw(self) -> None:
        self.clear()

        self.nb_disp.text = f"count: {self.nb: >30}"

        self.nb_disp.draw()

        size = 8

        for r in self.robots:
            i, j = r.pos
            arcade.draw_rect_filled(
                arcade.rect.XYWH(j * size + 30, self.height - (i * size) - 10, size-2, size-2),
                arcade.color.RED_DEVIL)


    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            self.pause = not self.pause

        if symbol == arcade.key.ESCAPE:
            arcade.exit()

        if symbol == arcade.key.ENTER:
            self.step = True

        if symbol == arcade.key.BACKSPACE or symbol == arcade.key.DELETE:
            self.rev_step = True

if __name__ == "__main__":
    test_size = V(7, 11)
    robot_test_1 = Robot(test_size, "p=2,4 v=2,-3")
    assert robot_test_1.advance(0) == V(4, 2)
    assert robot_test_1.advance(1) == V(1, 4)
    assert robot_test_1.advance(2) == V(5, 6)
    assert robot_test_1.advance(3) == V(2, 8)
    assert robot_test_1.advance(4) == V(6, 10)
    assert robot_test_1.advance(5) == V(3, 1)
    
    exem = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
    exems_robots = read_robots(7, 11, exem)
    exems_arrive = [r.advance(100) for r in exems_robots]
    arrival = {}
    for pos in exems_arrive:
        arrival[pos] = arrival.get(pos, 0) + 1
    
    assert arrival == {
        V(0,6): 2, V(0,9): 1, V(2,0): 1,
        V(3,1): 1, V(3,2): 1, V(4,5): 1,
        V(5,3): 1, V(5,4): 2, V(6,1): 1,
        V(6,6): 1
    }
    
    assert count_by_cadran(test_size, exems_arrive) == (1, 3, 4, 1)

    with open("input-14-1.txt") as f:
        print("first question:", pb1(f.read()))

    window = arcade.Window(1000, 900, "day 14")
    
    with open("input-14-1.txt") as f:
        game = MyView(103, 101, f.read())

    window.show_view(game)
    
    arcade.run()



# 115 14 -> 101