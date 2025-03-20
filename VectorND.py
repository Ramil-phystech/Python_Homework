from numbers import Real
from typing import Any, Iterable, Iterator, Union
from itertools import zip_longest


class VectorND:
    _vec: list  # list of vector components

    def __init__(self, iterable: Iterable[Real]):
        self._vec = list(iterable)

        if any(not isinstance(elem, Real) for elem in iterable):
            raise TypeError("Components of vector must be Real numbers")

        if len(self._vec) == 0:
            raise ValueError("A vector cannot be created "
                             "based on an empty iterable object")

    def __str__(self):
        s = ", ".join(str(x) for x in self._vec)

        if len(s) > 10:
            return f"VectorND({s[:10]}...)"

        return f"VectorND({s})"

    def __iter__(self) -> Iterator[Real]:
        return iter(self._vec)

    def __len__(self):
        return len(self._vec)

    def __contains__(self, index: Real) -> bool:
        if not isinstance(index, int):
            raise TypeError("The index of the vector component must be an integer")

        return 1 <= index <= len(self._vec)

    def __getitem__(self, n: int) -> Real:
        if not isinstance(n, int):
            raise TypeError("The index of the vector component must be an integer")

        if 1 <= n <= len(self._vec):
            return self._vec[n - 1]

        raise IndexError

    def __abs__(self) -> float:
        return sum(x ** 2 for x in self._vec) ** (1 / 2)

    def __float__(self) -> float:
        return float(abs(self))

    def __int__(self) -> int:
        return int(abs(self))

    def __bool__(self) -> bool:
        return abs(self) > 0

    def __eq__(self, other: 'VectorND') -> bool:
        if not isinstance(other, VectorND):
            raise TypeError

        c = list(zip_longest(self._vec, other._vec, fillvalue=0))

        return all(x[0] == x[1] for x in c)

    def __lt__(self, other: 'VectorND') -> bool:
        if not isinstance(other, VectorND):
            raise TypeError

        c = list(zip_longest(self._vec, other._vec, fillvalue=0))

        for i in range(len(c)):
            if c[i][0] < c[i][1] and all(c[j][0] == c[j][1] for j in range(i)):
                return True

            elif c[i][0] > c[i][1]:
                return False

        return False

    def __le__(self, other: 'VectorND') -> bool:
        if not isinstance(other, VectorND):
            raise TypeError

        return self < other or self == other

    def __mul__(self, num: Real) -> 'VectorND':
        if not isinstance(num, Real):
            raise TypeError

        return VectorND(x * num for x in self._vec)

    def __rmul__(self, num: Real) -> 'VectorND':
        return self * num

    def __truediv__(self, num: Real) -> 'VectorND':
        if not isinstance(num, Real):
            raise TypeError

        if num == 0:
            raise ZeroDivisionError

        return self * (1 / num)

    def __neg__(self) -> 'VectorND':
        return VectorND(-x for x in self._vec)

    def __add__(self, other: Union['VectorND', Real]) -> 'VectorND':
        if isinstance(other, Real):
            return VectorND(x + other for x in self._vec)
        if isinstance(other, VectorND):
            return VectorND(sum(x) for x in zip_longest(self._vec, other._vec, fillvalue=0))

        raise TypeError

    def __radd__(self, other: Union['VectorND', Real]) -> 'VectorND':
        return self + other

    def __sub__(self, other: Union['VectorND', Real]) -> 'VectorND':
        if isinstance(other, Real):
            return VectorND(x - other for x in self._vec)
        if isinstance(other, VectorND):
            return VectorND(x[0] - x[1] for x in zip_longest(self._vec, other._vec, fillvalue=0))

        raise TypeError

    def __rsub__(self, other: Union['VectorND', Real]) -> 'VectorND':
        return -self + other

    def __matmul__(self, other: 'VectorND') -> Real:
        if not isinstance(other, VectorND):
            raise TypeError

        return sum(x[0] * x[1] for x in zip_longest(self._vec, other._vec, fillvalue=0))
