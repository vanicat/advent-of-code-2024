class Processor:
    pc:int
    a:int
    b:int
    c:int

    instruction: list[int]
    output: list[int]

    def __init__(self, a, b, c, instruction:list[int]) -> None:
        self.pc = 0
        self.a = a
        self.b = b
        self.b_init = b
        self.c = c
        self.c_init = c

        self.instruction = instruction
        self.output = []

    def run(self, verbatim = False) -> list[int]:
        while self.step():
            if verbatim:
                if self.pc < len(self.instruction) and self.instruction[self.pc] == 5:
                    print(self.a, self.b, self.c, "out", self.b % 8)
                else:
                    print(self.a, self.b, self.c)

        return self.output


    def step(self):
        if self.pc not in range(0, len(self.instruction)):
            return False
        inst = self.instruction[self.pc]
        operande = self.instruction[self.pc + 1]
        match inst:
            case 0:
                self.adv(operande)
            case 1:
                self.bxl(operande)
            case 2:
                self.bst(operande)
            case 3:
                self.jnz(operande)
            case 4:
                self.bxc(operande)
            case 5:
                self.out(operande)
            case 6:
                self.bdv(operande)
            case 7:
                self.cdv(operande)
        return True


    def next(self):
        self.pc += 2

    def combo(self, operande):
        if operande < 4:
            return operande
        match operande:
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case x:
                raise ValueError("not a correcte operande : {x}")
    

    def adv(self, operande):
        numerator = self.a
        denominator = 2 ** self.combo(operande)
        self.a = numerator // denominator
        self.next()

    def bxl(self, operande):
        self.b = self.b  ^ operande
        self.next()

    def bst(self, operande):
        self.b = self.combo(operande) % 8
        self.next()

    def jnz(self, operande):
        if self.a != 0:
            self.pc = operande
        else:
            self.next()

    def bxc(self, operande):
        self.b = self.b  ^ self.c
        self.next()

    def out(self, operande):
        self.output.append(self.combo(operande) % 8)
        self.next()

    def bdv(self, operande):
        numerator = self.a
        denominator = 2 ** self.combo(operande)
        self.b = numerator // denominator
        self.next()

    def cdv(self, operande):
        numerator = self.a
        denominator = 2 ** self.combo(operande)
        self.c = numerator // denominator
        self.next()
        
    def reininit(self, a):
        self.output = []
        self.a = a
        self.b = self.b_init
        self.c = self.c_init
        self.pc = 0
    
def read_instruction(data:str) -> tuple[int, int, int, list[int]]:
    datas = (line.strip().split(" ") for line in data.strip().split("\n"))
    
    def read_register(line):
        assert line[0] == "Register"
        return int(line[-1])
    
    a = read_register(next(datas))
    b = read_register(next(datas))
    c = read_register(next(datas))

    assert next(datas) == ['']

    prgm, instr = next(datas)

    assert prgm == "Program:"
    instruction = [int(elem) for elem in instr.split(",")]
    return a, b, c, instruction

if __name__ == "__main__":
    proc = Processor(0, 0, 9, [2, 6])
    assert proc.step()
    assert not proc.step()
    assert proc.b == 1
 
    proc = Processor(0, 0, 9, [2, 6])
    assert proc.run() == []
    assert proc.b == 1
 
    proc = Processor(10, 0, 0, [5, 0, 5, 1, 5, 4])
    assert proc.run() == [0, 1, 2]
    
    proc = Processor(2024, 0, 0, [0,1,5,4,3,0])
    assert proc.run() == [4,2,5,6,7,7,7,7,3,1,0]
    assert proc.a == 0

    proc = Processor(0, 29, 0, [1,7])
    assert isinstance(proc.run(), list)
    assert proc.b == 26

    proc = Processor(0, 2024, 43690, [4, 0])
    assert isinstance(proc.run(), list)
    assert proc.b == 44354

    proc = Processor(*read_instruction("""
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""))
    assert proc.run() == [4,6,3,5,6,3,5,2,1,0]

    proc = Processor(*read_instruction("""
Register A: 64751475
Register B: 0
Register C: 0

Program: 2,4,1,2,7,5,4,5,1,3,5,5,0,3,3,0
"""))
    print("pb 1 soluce: ", ",".join(str(x) for x in proc.run()))

    a = 1
    result = []
    while len(proc.instruction) > len(result):
        a *= 2
        proc.reininit(a)
        result = proc.run()
        if True or a & 1111110 == 0:
            print("trying:", a, "result:", result)
    
    print(a)
    b = 1
    while proc.instruction != result:
        b *= 2
        proc.reininit(a + b)
        result = proc.run()
        if True or a + b & 1111110 == 0:
            print("trying:", a + b, "result:", result, proc.instruction)

    print(a+b)
    exit()
    proc.reininit(a)
    proc.run(True)
    start = a // 2
    end = a
    while end - start > 1:
        a = (start + end) // 2
        proc.reininit(a)
        result = proc.run()
        if result == proc.instruction:
            print("found", a)
        if len(result) < len(proc.instruction):
            start = a
        else:
            end = a


    print("find smallest good size", start, a, end, result)
    for a in range(start + 1, start + 10):
        proc.reininit(a)
        result = proc.run()
       
        proc.reininit(a)
        result = proc.run()
        if result[0:3] == [2, 4, 1]:
            print(a, result)
        if result == proc.instruction:
            print(a)


    proc.reininit(a)
    proc.run(True)

    proc.reininit(a+1)
    proc.run(True)