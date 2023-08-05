#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass


class JonesVector():
    def __init__(self, Jones):
        self.Jones = numpy.array(Jones)

    def __repr__(self):
        return self.Jones.__repr__()

    def __add__(self, Other):
        if self.Jones.ndim == 1 and Other.Jones.ndim == 1:
            return JonesVector([self.Jones, Other.Jones])

        if self.Jones.ndim == 2 and Other.Jones.ndim == 1:
            return JonesVector([*self.Jones, Other.Jones])

        if self.Jones.ndim == 1 and Other.Jones.ndim == 2:
            return JonesVector([self.Jones, *Other.Jones])

        if self.Jones.ndim == 2 and Other.Jones.ndim == 2:
            return JonesVector([*self.Jones, *Other.Jones])


class RightCircularPolarization(JonesVector):
    Description = 'Right circular polarization'

    def __init__(self):
        self.Jones = numpy.array([1, 1j]).astype(complex)


class LeftCircularPolarization(JonesVector):
    Description = 'Left circular polarization'

    def __init__(self):
        self.Jones = numpy.array([1, -1j]).astype(complex)


@dataclass
class LinearPolarization(JonesVector):
    Angles: list
    Unit: str = "Degree"

    def __post_init__(self):
        self.Angles = numpy.atleast_1d(self.Angles).astype(numpy.float64)

        if self.Unit.lower() == "degree":
            self.Angles = numpy.deg2rad(self.Angles, out=self.Angles, where=self.Angles!=numpy.nan)

        self.Jones = [[numpy.cos(angle), numpy.sin(angle)] for angle in self.Angles]
        self.Jones = numpy.asarray(self.Jones).astype(complex)

# -
