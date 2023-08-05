#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy

from PyMieSim.Tools.Polarization import LinearPolarization, JonesVector
from MPSPlots.Utils import ToList


@dataclass
class PlaneWave():
    r"""
    .. note::
        Class representing plane wave beam as a light source for
        light scattering.
    """

    Wavelength: float
    """ Wavelenght of the light field. """
    Polarization: float = 0
    """ Polarization of the light field in degree. """
    Amplitude: float = 1
    """ Maximal value of the electric field at focus point. """

    def __post_init__(self):
        self.k = 2 * numpy.pi / self.Wavelength
        self.Amplitude = ToList(self.Amplitude, dtype=numpy.float64)
        self.Polarization = ToList(self.Polarization, dtype=numpy.float64)
        self.Wavelength = ToList(self.Wavelength, dtype=numpy.float64)

        if isinstance(self.Polarization, JonesVector):
            self.Polarization = self.Polarization
        else:
            self.Polarization = LinearPolarization(Angles=self.Polarization)
