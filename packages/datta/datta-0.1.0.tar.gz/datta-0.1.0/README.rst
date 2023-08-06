.. logo_start
.. raw:: html

   <p align="center">
     <a href="https://github.com/brunonicko/datta">
         <picture>
            <object data="./_static/datta.svg" type="image/png">
                <source srcset="./docs/source/_static/datta_white.svg" media="(prefers-color-scheme: dark)">
                <img src="./docs/source/_static/datta.svg" width="60%" alt="datta" />
            </object>
         </picture>
     </a>
   </p>
.. logo_end

.. image:: https://github.com/brunonicko/datta/workflows/MyPy/badge.svg
   :target: https://github.com/brunonicko/datta/actions?query=workflow%3AMyPy

.. image:: https://github.com/brunonicko/datta/workflows/Lint/badge.svg
   :target: https://github.com/brunonicko/datta/actions?query=workflow%3ALint

.. image:: https://github.com/brunonicko/datta/workflows/Tests/badge.svg
   :target: https://github.com/brunonicko/datta/actions?query=workflow%3ATests

.. image:: https://readthedocs.org/projects/datta/badge/?version=stable
   :target: https://datta.readthedocs.io/en/stable/

.. image:: https://img.shields.io/github/license/brunonicko/datta?color=light-green
   :target: https://github.com/brunonicko/datta/blob/main/LICENSE

.. image:: https://static.pepy.tech/personalized-badge/datta?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads
   :target: https://pepy.tech/project/datta

.. image:: https://img.shields.io/pypi/pyversions/datta?color=light-green&style=flat
   :target: https://pypi.org/project/datta/

Overview
--------
Immutable data structures based on `estruttura <https://github.com/brunonicko/estruttura>`_.

Examples
--------

.. code:: python

    >>> from datta import Data, attribute
    >>> class Point(Data):
    ...     x = attribute(types=int)
    ...     y = attribute(types=int)
    ...
    >>> point_a = Point(3, 4)
    >>> point_a
    Point(3, 4)
    >>> point_b = point_a.update(x=30, y=40)
    >>> point_b
    Point(30, 40)

.. code:: python

    >>> from datta import Data, attribute, list_attribute
    >>> from tippo import Literal
    >>> class Vehicle(Data):
    ...     kind = attribute(types=str)
    ...
    >>> class Garage(Data):
    ...     vehicles = list_attribute(types=Vehicle)
    ...     gate = attribute(default="automatic", types=str)  # type: Literal["automatic", "manual"]
    ...
    >>> garage = Garage([Vehicle("bicycle"), Vehicle("car")], gate="manual")
    >>> garage
    Garage([Vehicle('bicycle'), Vehicle('car')], gate='manual')
    >>> garage.serialize() == {"vehicles": [{"kind": "bicycle"}, {"kind": "car"}], "gate": "manual"}
    True
    >>> Garage.deserialize({"vehicles": [{"kind": "bicycle"}, {"kind": "car"}], "gate": "manual"}) == garage
    True

.. code:: python

    >>> from datta import list_cls
    >>> MyStrList = list_cls(converter=str, qualified_name="MyStrList")
    >>> my_str_list = MyStrList([1, 2.2, None, True])
    >>> my_str_list
    MyStrList(['1', '2.2', 'None', 'True'])
