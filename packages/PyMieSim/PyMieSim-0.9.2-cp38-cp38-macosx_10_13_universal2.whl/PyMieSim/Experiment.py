#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from DataVisual import Xparameter
from dataclasses import dataclass
from DataVisual import DataV

from PyMieSim import LoadLPMode
from MPSPlots.Utils import ToList

from PyMieSim.Tools.Polarization import LinearPolarization
from PyMieSim.bin.Experiment import CppExperiment

from PyMieSim.bin.Sets import (CppCoreShellSet,
                               CppCylinderSet,
                               CppSphereSet,
                               CppSourceSet,
                               CppDetectorSet)


@dataclass
class CoreShellSet():
    core_diameter: list
    """ diameter of the core of the single scatterer [m]. """
    shell_diameter: list
    """ diameter of the shell of the single scatterer [m]. """
    core_index: list = None
    """ Refractive index of the core of the scatterer. """
    shell_index: list = None
    """ Refractive index of the shell of the scatterer. """
    core_material: list = None
    """ Core material of which the scatterer is made of. Only if core_index is not specified.  """
    shell_material: list = None
    """ Shell material of which the scatterer is made of. Only if shell_index is not specified.  """
    n_medium: list = 1.0
    """ Refractive index of scatterer medium. """
    name: str = 'coreshell'
    """name of the set """

    def __post_init__(self):
        self.bounded_core = True if self.core_material is not None else False
        self.bounded_shell = True if self.shell_material is not None else False

        self.core_diameter = Xparameter(values=ToList(self.core_diameter, dtype=numpy.float64),
                                       name='diameter',
                                       format=".2e",
                                       unit="m",
                                       long_label='diameter',
                                       short_label='diameter')

        self.shell_diameter = Xparameter(values=ToList(self.shell_diameter, dtype=numpy.float64),
                                        name='Shell diameter',
                                        format=".2e",
                                        unit="m",
                                        long_label='Shell diameter',
                                        short_label='Shell diameter')

        self.core_material = Xparameter(values=ToList(self.core_material, dtype=None),
                                       name='core_material',
                                       format="",
                                       unit="",
                                       long_label='core_material',
                                       short_label='core_material')

        self.shell_material = Xparameter(values=ToList(self.shell_material, dtype=None),
                                        name='shell_material',
                                        format="",
                                        unit="",
                                        long_label='shell_material',
                                        short_label='shell_material')

        self.core_index = Xparameter(values=ToList(self.core_index, dtype=numpy.complex128),
                                    name='core_index',
                                    format="",
                                    unit="1",
                                    long_label='core_index',
                                    short_label='core_index')

        self.shell_index = Xparameter(values=ToList(self.shell_index, dtype=numpy.complex128),
                                     name='shell_index',
                                     format="",
                                     unit="1",
                                     long_label='shell_index',
                                     short_label='shell_index')

        self.n_medium = Xparameter(values=ToList(self.n_medium, dtype=numpy.float64),
                                  name='n_medium',
                                  long_label='n_medium',
                                  format=".2f",
                                  unit="1",
                                  short_label='n_medium')

    def _bind_to_experiment_(self, Experiment):
        Experiment.Binding.set_coreshell(self.Binding)

    def Evaluate(self, Source):
        if self.bounded_core and self.bounded_shell:
            core_material = numpy.asarray([material.GetRI(Source.values) for material in self.core_material])
            shell_material = numpy.asarray([material.GetRI(Source.values) for material in self.shell_material])

            self.Binding = CppCoreShellSet(core_diameter=self.core_diameter.values,
                                           shell_diameter=self.shell_diameter.values,
                                           core_material=core_material.astype(complex),
                                           shell_material=shell_material.astype(complex),
                                           n_medium=self.n_medium.values)

        if self.bounded_core and not self.bounded_shell:
            core_material = numpy.asarray([material.GetRI(Source.values) for material in self.core_material])

            self.Binding = CppCoreShellSet(core_diameter=self.core_diameter.values,
                                           shell_diameter=self.shell_diameter.values,
                                           core_material=core_material.astype(complex),
                                           shell_index=self.shell_index.values,
                                           n_medium=self.n_medium.values)

        if not self.bounded_core and self.bounded_shell:
            shell_material = numpy.asarray([material.GetRI(Source.values) for material in self.shell_material])

            self.Binding = CppCoreShellSet(core_diameter=self.core_diameter.values,
                                           shell_diameter=self.shell_diameter.values,
                                           core_index=self.core_index.values,
                                           shell_material=shell_material.astype(complex),
                                           n_medium=self.n_medium.values)

        if not self.bounded_core and not self.bounded_shell:
            self.Binding = CppCoreShellSet(core_diameter=self.core_diameter.values,
                                           shell_diameter=self.shell_diameter.values,
                                           core_index=self.core_index.values,
                                           shell_index=self.shell_index.values,
                                           n_medium=self.n_medium.values)

    def __append_to_table__(self, Table):
        if self.bounded_core and self.bounded_shell:
            return [*Table, self.core_diameter, self.shell_diameter, self.core_material, self.shell_material, self.n_medium]

        if self.bounded_core and not self.bounded_shell:
            return [*Table, self.core_diameter, self.shell_diameter, self.core_material, self.shell_index, self.n_medium]

        if not self.bounded_core and self.bounded_shell:
            return [*Table, self.core_diameter, self.shell_diameter, self.core_index, self.shell_material, self.n_medium]

        if not self.bounded_core and not self.bounded_shell:
            return [*Table, self.core_diameter, self.shell_diameter, self.core_index, self.shell_index, self.n_medium]


@dataclass
class SphereSet():
    diameter: list
    """ diameter of the single scatterer in unit of meter. """
    index: list = None
    """ Refractive index of scatterer. """
    material: list = None
    """ material of which the scatterer is made of. Only if index is not specified. """
    n_medium: list = 1.0
    """ Refractive index of scatterer medium. """
    name: str = 'sphere'
    """name of the set """

    def __post_init__(self):
        self.Boundedindex = True if self.material is not None else False

        self.diameter = Xparameter(values=ToList(self.diameter, dtype=numpy.float64),
                                   name='diameter',
                                   format=".2e",
                                   unit="m",
                                   long_label='diameter',
                                   short_label='diameter')

        self.material = Xparameter(values=ToList(self.material, dtype=None),
                                   name='material',
                                   format="",
                                   unit="",
                                   long_label='material',
                                   short_label='material')

        self.index = Xparameter(values=ToList(self.index, dtype=numpy.complex128),
                                name='index',
                                format="",
                                unit="1",
                                long_label='index',
                                short_label='index')

        self.n_medium = Xparameter(values=ToList(self.n_medium, dtype=numpy.float64),
                                  name='n_medium',
                                  long_label='n_medium',
                                  format=".2f",
                                  unit="1",
                                  short_label='n_medium')

    def _bind_to_experiment_(self, Experiment):
        Experiment.Binding.set_sphere(self.Binding)

    def Evaluate(self, Source):
        if self.Boundedindex:
            material = numpy.asarray([material.GetRI(Source.values) for material in self.material])

            self.Binding = CppSphereSet(diameter=self.diameter.values.astype(float),
                                        material=material.astype(complex),
                                        n_medium=self.n_medium.values.astype(float))

        else:
            self.Binding = CppSphereSet(diameter=self.diameter.values,
                                        index=self.index.values,
                                        n_medium=self.n_medium.values)

    def __append_to_table__(self, Table):
        if self.Boundedindex:
            return [*Table, self.diameter, self.material, self.n_medium]

        else:
            return [*Table, self.diameter, self.index, self.n_medium]


@dataclass
class CylinderSet():
    diameter: list
    """ diameter of the single scatterer in unit of meter. """
    index: list = None
    """ Refractive index of scatterer. """
    material: list = None
    """ Refractive index of scatterer medium. """
    n_medium: list = 1.0
    """ material of which the scatterer is made of. Only if index is not specified. """
    name: str = 'cylinder'
    """name of the set """

    def __post_init__(self):
        self.Boundedindex = True if self.material is not None else False

        self.diameter = Xparameter(values=ToList(self.diameter, dtype=numpy.float64),
                                   name='diameter',
                                   format=".2e",
                                   unit="m",
                                   long_label='diameter',
                                   short_label='diameter')

        self.material = Xparameter(values=ToList(self.material, dtype=None),
                                   name='material',
                                   format="",
                                   unit="",
                                   long_label='material',
                                   short_label='material')

        self.index = Xparameter(values=ToList(self.index, dtype=numpy.complex128),
                                name='index',
                                format="",
                                unit="1",
                                long_label='index',
                                short_label='index')

        self.n_medium = Xparameter(values=ToList(self.n_medium, dtype=numpy.float64),
                                  name='n_medium',
                                  long_label='n_medium',
                                  format=".2f",
                                  unit="1",
                                  short_label='n_medium')

    def _bind_to_experiment_(self, Experiment):
        Experiment.Binding.set_cylinder(self.Binding)

    def Evaluate(self, Source):
        if self.Boundedindex:
            material = numpy.asarray([material.GetRI(Source.values) for material in self.material])

            self.Binding = CppCylinderSet(diameter=self.diameter.values.astype(float),
                                          material=material.astype(complex),
                                          n_medium=self.n_medium.values.astype(float))

        else:
            self.Binding = CppCylinderSet(diameter=self.diameter.values,
                                          index=self.index.values,
                                          n_medium=self.n_medium.values)

    def __append_to_table__(self, Table):
        if self.Boundedindex:
            return [*Table, self.diameter, self.material, self.n_medium]

        else:
            return [*Table, self.diameter, self.index, self.n_medium]


@dataclass
class SourceSet(object):
    wavelength: float = 1.0
    """ Wavelenght of the light field. """
    polarization: float = None
    """ polarization of the light field in degree. """
    amplitude: float = None
    """ Maximal value of the electric field at focus point. """
    name: str = 'PlaneWave'
    """ name of the set """

    def __post_init__(self):
        self.polarization = LinearPolarization(self.polarization)

        self.wavelength = Xparameter(values=ToList(self.wavelength, dtype=numpy.float64),
                                     name='wavelength',
                                     long_label='wavelength',
                                     format=".1e",
                                     unit="m",
                                     short_label='wavelength')

        self.polarization = Xparameter(values=ToList(self.polarization.jones_vector, dtype=numpy.complex128),
                                       representation=ToList(self.polarization.angle_list, dtype=numpy.float64),
                                       name='polarization',
                                       long_label='polarization',
                                       format=".1f",
                                       unit="Deg",
                                       short_label='polarization')

        self.amplitude = Xparameter(values=ToList(self.amplitude, dtype=numpy.float64),
                                    name='amplitude',
                                    long_label='amplitude',
                                    format=".1e",
                                    unit="w.m⁻¹",
                                    short_label='amplitude')

        self.Binding = CppSourceSet(wavelength=self.wavelength.values,
                                    jones_vector=self.polarization.values,
                                    amplitude=self.amplitude.values)

    def _bind_to_experiment_(self, Experiment):
        Experiment.Binding.set_source(self.Binding)

    def __append_to_table__(self, Table):
        return [*Table, self.wavelength, self.polarization, self.amplitude]


@dataclass
class PhotodiodeSet():
    NA: list
    """ Numerical aperture of imaging system. """
    gamma_offset: list
    """ Angle [Degree] offset of detector in the direction perpendicular to polarization. """
    phi_offset: list
    """ Angle [Degree] offset of detector in the direction parallel to polarization. """
    filter: list
    """ Angle [Degree] of polarization filter in front of detector. """
    coupling_mode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    coherent: bool = False
    """ Describe the detection scheme coherent or uncoherent. """
    sampling: int = 200
    """ Describe the detection scheme coherent or uncoherent. """
    name = "LPMode"
    """ name of the set """

    def __post_init__(self):

        self.scalarfield = Xparameter(values=numpy.asarray([numpy.ones(self.sampling)]),
                                      representation=ToList('Photodiode', dtype=str),
                                      name='Field',
                                      long_label='Coupling field',
                                      format="",
                                      unit="",
                                      short_label='C.F')

        self.NA = Xparameter(values=ToList(self.NA, dtype=numpy.float64),
                             name='NA',
                             long_label='Numerical aperture',
                             format=".3f",
                             unit="Rad",
                             short_label='NA')

        self.phi_offset = Xparameter(values=ToList(self.phi_offset, dtype=numpy.float64),
                                    name='phi_offset',
                                    long_label='Phi offset',
                                    format="03.1f",
                                    unit="Deg",
                                    short_label='Phi offset')

        self.gamma_offset = Xparameter(values=ToList(self.gamma_offset, dtype=numpy.float64),
                                      name='gamma_offset',
                                      long_label='Gamma offset',
                                      format="03.1f",
                                      unit="Deg",
                                      short_label='Gamma offset')

        self.filter = Xparameter(values=ToList(self.filter, dtype=numpy.float64),
                                 name='filter',
                                 long_label='filter',
                                 format="03.1f",
                                 unit="Deg",
                                 short_label='filter angle')

        self.__bind_to_cpp__()

    def __bind_to_cpp__(self):
        self.Binding = CppDetectorSet(scalarfield=self.scalarfield.values,
                                      NA=self.NA.values,
                                      phi_offset=numpy.deg2rad(self.phi_offset.values),
                                      gamma_offset=numpy.deg2rad(self.gamma_offset.values),
                                      filter=numpy.array([x if x is not None else numpy.nan for x in self.filter.values]),
                                      point_coupling=True if self.coupling_mode == 'Point' else False,
                                      coherent=self.coherent)

    def _bind_to_experiment_(self, Experiment):
        Experiment.Binding.set_detector(self.Binding)

    def __append_to_table__(self, Table):
        return [*Table, self.scalarfield, self.NA, self.phi_offset, self.gamma_offset, self.filter]


@dataclass
class LPModeSet():
    Mode: list
    """ List of mode to be used. """
    NA: list
    """ Numerical aperture of imaging system. """
    gamma_offset: list
    """ Angle [Degree] offset of detector in the direction perpendicular to polarization. """
    phi_offset: list
    """ Angle [Degree] offset of detector in the direction parallel to polarization. """
    filter: list
    """ Angle [Degree] of polarization filter in front of detector. """
    coupling_mode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    coherent: bool = False
    """ Describe the detection scheme coherent or uncoherent. """
    sampling: int = 200
    """ Describe the detection scheme coherent or uncoherent. """
    name = "LPMode"
    """ name of the set """

    def __post_init__(self):

        self.scalarfield = Xparameter(values=numpy.asarray([LoadLPMode(mode_number=mode, sampling=self.sampling, type='unstructured') for mode in ToList(self.Mode)]),
                                      representation=ToList(self.Mode, dtype=str),
                                      name='Field',
                                      long_label='Coupling field',
                                      format="",
                                      unit="",
                                      short_label='C.F')

        self.NA = Xparameter(values=ToList(self.NA, dtype=numpy.float64),
                             name='NA',
                             long_label='Numerical aperture',
                             format=".3f",
                             unit="Rad",
                             short_label='NA')

        self.phi_offset = Xparameter(values=ToList(self.phi_offset, dtype=numpy.float64),
                                    name='phi_offset',
                                    long_label='Phi offset',
                                    format="03.1f",
                                    unit="Deg",
                                    short_label='Phi offset')

        self.gamma_offset = Xparameter(values=ToList(self.gamma_offset, dtype=numpy.float64),
                                      name='gamma_offset',
                                      long_label='Gamma offset',
                                      format="03.1f",
                                      unit="Deg",
                                      short_label='Gamma offset')

        self.filter = Xparameter(values=ToList(self.filter, dtype=numpy.float64),
                                 name='filter',
                                 long_label='filter',
                                 format="03.1f",
                                 unit="Deg",
                                 short_label='filter angle')

        self.__bind_to_cpp__()

    def __bind_to_cpp__(self):
        self.Binding = CppDetectorSet(scalarfield=self.scalarfield.values,
                                      NA=self.NA.values,
                                      phi_offset=numpy.deg2rad(self.phi_offset.values),
                                      gamma_offset=numpy.deg2rad(self.gamma_offset.values),
                                      filter=numpy.array([x if x is not None else numpy.nan for x in self.filter.values]),
                                      point_coupling=True if self.coupling_mode == 'Point' else False,
                                      coherent=self.coherent)

    def _bind_to_experiment_(self, Experiment):
        Experiment.Binding.set_detector(self.Binding)

    def __append_to_table__(self, Table):
        return [*Table, self.scalarfield, self.NA, self.phi_offset, self.gamma_offset, self.filter]


class Setup(object):
    def __init__(self, scatterer_set=None, source_set=None, detector_set=None):

        self.source_set = source_set

        self.detector_set = detector_set

        self.scatterer_set = scatterer_set

        self.scatterer_set.Evaluate(self.source_set.wavelength)

        self.Binding = CppExperiment()

        self._bind_element_()

        self.x_table = self.source_set.__append_to_table__([])
        self.x_table = self.scatterer_set.__append_to_table__(self.x_table)

        if self.detector_set is not None:
            self.x_table = self.detector_set.__append_to_table__(self.x_table)

    def _bind_element_(self):
        self.source_set._bind_to_experiment_(self)
        self.scatterer_set._bind_to_experiment_(self)

        if self.detector_set:
            self.detector_set._bind_to_experiment_(self)

    def Get(self, Input: list) -> DataV:
        """Methode generate array of the givens parameters as a function of
        all independent variables.

        """

        Input = ToList(Input)

        self.y_table = Input

        Array = []
        for prop in Input:
            prop.values = numpy.array([])

            prop = 'get' + "_" + self.scatterer_set.name + "_" + prop.name

            sub_array = getattr(self.Binding, prop)()

            Array.append(sub_array)

        Array = numpy.asarray(Array)

        for n, e in enumerate(self.x_table):
            e.position = n + 1

        return DataV(Array, x_table=self.x_table, y_table=self.y_table)
