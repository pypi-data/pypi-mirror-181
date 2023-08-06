import math



def cos(a):
    return math.cos(math.radians(a))

def sin(a):
    return math.sin(math.radians(a))

def sgn(a):
    return a/abs(a) if a != 0 else 0

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def check_instance(fun):
        def wrap(self, other):
            if not isinstance(other, Vector):
                raise TypeError("types don't match")
            return fun(self, other)
        return wrap

    @check_instance
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    @check_instance
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Vector(self.x / other, self.y / other)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __str__(self):
        return "Vector object with coords ({}, {})".format(self.x, self.y)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    @property
    def unit(self):
        return self / abs(self) if abs(self) != 0 else Vector.ZERO()

    @classmethod
    def ZERO(cls):
        return cls(0, 0)