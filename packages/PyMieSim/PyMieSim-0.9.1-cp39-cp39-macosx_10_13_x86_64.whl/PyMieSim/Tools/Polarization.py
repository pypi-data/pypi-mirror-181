#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass


class JonesVector():
    def __init__(self, jones_vector):
        self.jones_vector = numpy.array(jones_vector)

    def __repr__(self):
        return self.jones_vector.__repr__()

    def __add__(self, Other):
        if self.jones_vector.ndim == 1 and Other.jones_vector.ndim == 1:
            return JonesVector([self.jones_vector, Other.jones_vector])

        if self.jones_vector.ndim == 2 and Other.jones_vector.ndim == 1:
            return JonesVector([*self.jones_vector, Other.jones_vector])

        if self.jones_vector.ndim == 1 and Other.jones_vector.ndim == 2:
            return JonesVector([self.jones_vector, *Other.jones_vector])

        if self.jones_vector.ndim == 2 and Other.jones_vector.ndim == 2:
            return JonesVector([*self.jones_vector, *Other.jones_vector])


class RightCircularPolarization(JonesVector):
    Description = 'Right circular polarization'

    def __init__(self):
        self.jones_vector = numpy.array([1, 1j]).astype(complex)


class LeftCircularPolarization(JonesVector):
    Description = 'Left circular polarization'

    def __init__(self):
        self.jones_vector = numpy.array([1, -1j]).astype(complex)


@dataclass
class LinearPolarization(JonesVector):
    angle_list: list
    Unit: str = "Degree"

    def __post_init__(self):
        self.angle_list = numpy.atleast_1d(self.angle_list).astype(numpy.float64)

        if self.Unit.lower() == "degree":
            self.angle_list = numpy.deg2rad(self.angle_list, out=self.angle_list, where=self.angle_list != numpy.nan)

        self.jones_vector = [[numpy.cos(angle), numpy.sin(angle)] for angle in self.angle_list]
        self.jones_vector = numpy.asarray(self.jones_vector).astype(complex)

# -
