import random


class LzRandomImp(object):

    # [ 0 : 1 )
    def random(self) -> float:
        return random.random()

    # [ start : end )
    def random_float_range(self, start: float, end: float) -> float:
        return random.uniform(start, end)

    # [ start : end ]
    def random_int_range(self, start: int, end: int, step: int = 1) -> int:
        r = random.randint(start, end)
        num = start
        while num < end and num <= r:
            num += step

        num = num - step if num >= end else num

        r1 = num - step
        r2 = num

        n2 = abs(r - num)
        n1 = n2
        if num - step >= start:
            n1 = abs(r - (num - step))

        res = None
        if n1 == n2:
            res = random.choice([r1, r2])
        elif n1 < n2:
            res = r1
        else:
            res = r2

        return res

# lz = LzRandomImp()
#
# print(lz.random_int_range(1, 10, 2))
