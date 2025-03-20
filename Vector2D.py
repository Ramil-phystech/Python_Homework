from dataclasses import dataclass
from math import acos, pi
from typing import Union
from numbers import Real


class Vector2D:
    _ordinate: float
    _abscissa: float

    def __init__(self, abscissa: float = 0.0, ordinate: float = 0.0) -> None:
        self._abscissa = float(abscissa)
        self._ordinate = float(ordinate)

    @property
    def ordinate(self) -> float:
        return self._ordinate

    @property
    def abscissa(self) -> float:
        return self._abscissa

    def __str__(self) -> str:
        return fr"Vector2D(abscissa={self._abscissa}, ordinate={self._ordinate})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2D):
            raise TypeError

        return self._ordinate == other._ordinate and self._abscissa == other._abscissa

    def __lt__(self, other: 'Vector2D') -> bool:
        if not isinstance(other, Vector2D):
            raise TypeError

        return self._abscissa < other._abscissa or (self._abscissa == other._abscissa
                                                    and self._ordinate < other._ordinate)

    def __le__(self, other: 'Vector2D') -> bool:
        if not isinstance(other, Vector2D):
            raise TypeError

        return self < other or self == other

    def __abs__(self) -> float:
        return (self._abscissa ** 2 + self._ordinate ** 2) ** (1 / 2)

    def __bool__(self) -> bool:
        return abs(self) > 0

    def __mul__(self, other: Real) -> 'Vector2D':
        if not isinstance(other, Real):
            return NotImplemented

        return Vector2D(self._abscissa * other, self._ordinate * other)

    def __rmul__(self, other: Real) -> 'Vector2D':
        return self * other

    def __add__(self, other: Union[Real, 'Vector2D']) -> 'Vector2D':
        if isinstance(other, Real):
            return Vector2D(self._abscissa + other, self._ordinate + other)

        if isinstance(other, Vector2D):
            return Vector2D(self._abscissa + other._abscissa, self._ordinate + other._ordinate)

        return NotImplemented

    def __radd__(self, other) -> 'Vector2D':
        return self + other

    def __truediv__(self, other: Real) -> 'Vector2D':
        if not isinstance(other, Real):
            return NotImplemented

        return self * (1 / other)

    def __neg__(self) -> 'Vector2D':
        return Vector2D(-self._abscissa, -self._ordinate)

    def __sub__(self, other: Union['Vector2D', Real]) -> 'Vector2D':
        if isinstance(other, Real):
            return Vector2D(self._abscissa - other, self._ordinate - other)

        if isinstance(other, Vector2D):
            return Vector2D(self._abscissa - other._abscissa, self._ordinate - other._ordinate)

        return NotImplemented

    def __rsub__(self, other: Union['Vector2D', Real]) -> 'Vector2D':
        return -self + other

    def __complex__(self) -> complex:
        return complex(real=self._abscissa, imag=self._ordinate)

    def __float__(self) -> float:
        return abs(self)

    def __int__(self) -> int:
        return int(abs(self))

    def __matmul__(self, other: 'Vector2D') -> float:
        if not isinstance(other, Vector2D):
            return NotImplemented

        return self._abscissa * other._abscissa + self._ordinate * other._ordinate

    def get_angle(self, other: 'Vector2D') -> Real:
        if not isinstance(other, Vector2D):
            raise ValueError

        if abs(self) == 0 or abs(other) == 0:
            raise ValueError("It is impossible to calculate the angle for the zero vector")

        return acos(self @ other / (abs(self) * abs(other))) * 180 / pi

    def conjugate(self) -> 'Vector2D':
        return Vector2D(self._abscissa, -self._ordinate)