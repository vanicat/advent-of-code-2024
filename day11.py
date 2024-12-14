from collections.abc import Generator, Iterable
from typing import Optional, Sequence


def blink(it:Iterable) -> Generator[int]:
    for value in it:      
        if value == 0:
            yield 1
        elif len(st:=str(value)) % 2 == 0:
            yield int(st[:len(st) // 2])
            yield int(st[len(st) // 2:])
        else:
            yield value * 2024


def len_iterable(it:Iterable) -> int:
    nb = 0
    for _ in it:
        nb += 1

    return nb


def sequence_from_str(data:str) -> Generator[int]:
    for elem in data.strip().split(" "):
        yield int(elem)


if __name__ == "__main__":

    exem1 = list(sequence_from_str("125 17"))
    assert exem1 == [125, 17]
    exem1 = list(blink(exem1))
    assert exem1 == list(sequence_from_str("253000 1 7"))
    exem1 = list(blink(exem1))
    assert exem1 == list(sequence_from_str("253 0 2024 14168"))
    exem1 = list(blink(exem1))
    assert exem1 == list(sequence_from_str("512072 1 20 24 28676032"))
    exem1 = list(blink(exem1))
    assert exem1 == list(sequence_from_str("512 72 2024 2 0 2 4 2867 6032"))
    exem1 = list(blink(exem1))
    assert exem1 == list(sequence_from_str("1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32"))
    exem1 = list(blink(exem1))
    assert exem1 == list(sequence_from_str("2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2"))
    assert len(exem1) == 22
    for i in range(6, 25):
        exem1 = blink(exem1)
    assert len_iterable(exem1) == 55312 # type: ignore

    pb_input:str = "8793800 1629 65 5 960 0 138983 85629"
    pb = sequence_from_str(pb_input)

    for _ in range(25):
        pb = blink(pb)
    
    print("problem 1 score is", len_iterable(pb))

    pb = sequence_from_str(pb_input)

    for _ in range(75):
        pb = blink(pb)
    
    print("problem 1 score is", len_iterable(pb))
