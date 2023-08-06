from __future__ import absolute_import, division, print_function

import pytest

from datta import Data, attribute, exceptions, getter


def test_datta():
    class Point(Data):
        x = attribute()
        y = attribute()

    point = Point(3, 4)
    assert point == Point(3, 4)


def test_attributes():
    class A(Data):
        x = attribute()

    class B(A):
        y = attribute()

    class C(B):
        z = attribute()

    assert list(C.__attribute_map__.items()) == [
        ("x", A.__attribute_map__["x"]),
        ("y", B.__attribute_map__["y"]),
        ("z", C.__attribute_map__["z"]),
    ]

    with pytest.raises(TypeError):

        class D(C):
            x = 0

        assert not D  # type: ignore


def test_constants():
    class Circle(Data):
        PI = attribute(3.14, constant=True)
        radius = attribute(types=float)
        circumference = attribute()

        @getter(circumference, dependencies=(PI, radius))
        def _(self):
            return 2 * self.PI * self.radius

    circle = Circle(3.0)
    assert circle.circumference == 18.84

    with pytest.raises(AttributeError):
        Circle.PI = 5

    with pytest.raises(AttributeError):
        circle.PI = 5


def test_evolve():
    class Point(Data):
        x = attribute()
        y = attribute()

    point = Point(3, 4)
    with pytest.raises(AttributeError):
        point.x = 30

    new_point = point.set("x", 30)
    assert isinstance(new_point, Point)
    assert new_point.x == 30
    assert point.x == 3


def test_type_checking():
    class Point(Data):
        x = attribute(types=int)
        y = attribute(types=int)

    point = Point(3, 4)

    with pytest.raises(exceptions.InvalidTypeError):
        point.set("x", 3.0)


if __name__ == "__main__":
    pytest.main()
