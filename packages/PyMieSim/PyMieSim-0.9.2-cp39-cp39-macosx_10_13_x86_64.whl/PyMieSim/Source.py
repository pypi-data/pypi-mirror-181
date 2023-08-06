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

    wavelength: float
    """ Wavelenght of the light field. """
    polarization: float = 0
    """ Polarization of the light field in degree. """
    amplitude: float = 1
    """ Maximal value of the electric field at focus point. """

    def __post_init__(self):
        self.k = 2 * numpy.pi / self.wavelength
        self.amplitude = ToList(self.amplitude, dtype=numpy.float64)
        self.polarization = ToList(self.polarization, dtype=numpy.float64)
        self.wavelength = ToList(self.wavelength, dtype=numpy.float64)

        if isinstance(self.polarization, JonesVector):
            self.polarization = self.polarization
        else:
            self.polarization = LinearPolarization(angle_list=self.polarization)
