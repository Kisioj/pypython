import dis

class Dupa:
    x = ...
    y = "ale jajca"

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

x, y = 5, 10
z = ...
def foo(bar, z=..., car=[1337, 1338, 1339]):
    a = bar + 1
    return a - x, car
print(y * foo(2))

def hehe(x, y=25, *, z=20, u):
    yield x
    yield y
    return [z, u] * 50

dupa = Dupa(cwel=12.5)
print(dupa.cwel, end='hehe')
input('Ohujałeś kurwa pierdolony kurwiu?')

def nop():
    pass
