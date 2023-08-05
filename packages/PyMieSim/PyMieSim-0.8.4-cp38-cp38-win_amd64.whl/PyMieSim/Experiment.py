#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DataVisual import XParameter
from dataclasses import dataclass
import numpy
import PyOptik
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
    CoreDiameter: list
    """ Diameter of the core of the single scatterer [m]. """
    ShellDiameter: list
    """ Diameter of the shell of the single scatterer [m]. """
    CoreIndex: list = None
    """ Refractive index of the core of the scatterer. """
    ShellIndex: list = None
    """ Refractive index of the shell of the scatterer. """
    CoreMaterial: list = None
    """ Core material of which the scatterer is made of. Only if CoreIndex is not specified.  """
    ShellMaterial: list = None
    """ Shell material of which the scatterer is made of. Only if ShellIndex is not specified.  """
    nMedium: list = 1.0
    """ Refractive index of scatterer medium. """
    Name: str = 'coreshell'
    """Name of the set """

    def __post_init__(self):
        self.BoundedCore = True if self.CoreMaterial is not None else False
        self.BoundedShell = True if self.ShellMaterial is not None else False

        self.CoreDiameter = XParameter(Values=ToList(self.CoreDiameter, dtype=numpy.float64),
                                       Name='Diameter',
                                       Format=".2e",
                                       Unit="m",
                                       LongLabel='Diameter',
                                       Legend='Diameter',
                                       Type=numpy.float64)

        self.ShellDiameter = XParameter(Values=ToList(self.ShellDiameter, dtype=numpy.float64),
                                        Name='Shell Diameter',
                                        Format=".2e",
                                        Unit="m",
                                        LongLabel='Shell Diameter',
                                        Legend='Shell Diameter',
                                        Type=numpy.float64)

        self.CoreMaterial = XParameter(Values=ToList(self.CoreMaterial, dtype=None),
                                       Name='CoreMaterial',
                                       Format="",
                                       Unit="",
                                       LongLabel='CoreMaterial',
                                       Legend='CoreMaterial',
                                       Type=PyOptik.ExpData)

        self.ShellMaterial = XParameter(Values=ToList(self.ShellMaterial, dtype=None),
                                        Name='ShellMaterial',
                                        Format="",
                                        Unit="",
                                        LongLabel='ShellMaterial',
                                        Legend='ShellMaterial',
                                        Type=PyOptik.ExpData)

        self.CoreIndex = XParameter(Values=ToList(self.CoreIndex, dtype=numpy.complex128),
                                    Name='CoreIndex',
                                    Format="",
                                    Unit="1",
                                    LongLabel='CoreIndex',
                                    Legend='CoreIndex',
                                    Type=numpy.complex128)

        self.ShellIndex = XParameter(Values=ToList(self.ShellIndex, dtype=numpy.complex128),
                                     Name='ShellIndex',
                                     Format="",
                                     Unit="1",
                                     LongLabel='ShellIndex',
                                     Legend='ShellIndex',
                                     Type=numpy.complex128)

        self.nMedium = XParameter(Values=ToList(self.nMedium, dtype=numpy.float64),
                                  Name='nMedium',
                                  LongLabel='nMedium',
                                  Format=".2f",
                                  Unit="1",
                                  Legend='nMedium',
                                  Type=numpy.float64)

    def BindToExperiment(self, Experiment):
        Experiment.Binding.set_coreshell(self.Binding)

    def Evaluate(self, Source):
        if self.BoundedCore and self.BoundedShell:
            CoreMaterial = numpy.asarray([material.GetRI(Source.Values) for material in self.CoreMaterial])
            ShellMaterial = numpy.asarray([material.GetRI(Source.Values) for material in self.ShellMaterial])

            self.Binding = CppCoreShellSet(CoreDiameter=self.CoreDiameter.Values,
                                           ShellDiameter=self.ShellDiameter.Values,
                                           CoreMaterial=CoreMaterial.astype(complex),
                                           ShellMaterial=ShellMaterial.astype(complex),
                                           nMedium=self.nMedium.Values)

        if self.BoundedCore and not self.BoundedShell:
            CoreMaterial = numpy.asarray([material.GetRI(Source.Values) for material in self.CoreMaterial])

            self.Binding = CppCoreShellSet(CoreDiameter=self.CoreDiameter.Values,
                                           ShellDiameter=self.ShellDiameter.Values,
                                           CoreMaterial=CoreMaterial.astype(complex),
                                           ShellIndex=self.ShellIndex.Values,
                                           nMedium=self.nMedium.Values)

        if not self.BoundedCore and self.BoundedShell:
            ShellMaterial = numpy.asarray([material.GetRI(Source.Values) for material in self.ShellMaterial])

            self.Binding = CppCoreShellSet(CoreDiameter=self.CoreDiameter.Values,
                                           ShellDiameter=self.ShellDiameter.Values,
                                           CoreIndex=self.CoreIndex.Values,
                                           ShellMaterial=ShellMaterial.astype(complex),
                                           nMedium=self.nMedium.Values)

        if not self.BoundedCore and not self.BoundedShell:
            self.Binding = CppCoreShellSet(CoreDiameter=self.CoreDiameter.Values,
                                           ShellDiameter=self.ShellDiameter.Values,
                                           CoreIndex=self.CoreIndex.Values,
                                           ShellIndex=self.ShellIndex.Values,
                                           nMedium=self.nMedium.Values)

    def __append_to_table__(self, Table):
        if self.BoundedCore and self.BoundedShell:
            return [*Table, self.CoreDiameter, self.ShellDiameter, self.CoreMaterial, self.ShellMaterial, self.nMedium]

        if self.BoundedCore and not self.BoundedShell:
            return [*Table, self.CoreDiameter, self.ShellDiameter, self.CoreMaterial, self.ShellIndex, self.nMedium]

        if not self.BoundedCore and self.BoundedShell:
            return [*Table, self.CoreDiameter, self.ShellDiameter, self.CoreIndex, self.ShellMaterial, self.nMedium]

        if not self.BoundedCore and not self.BoundedShell:
            return [*Table, self.CoreDiameter, self.ShellDiameter, self.CoreIndex, self.ShellIndex, self.nMedium]


@dataclass
class SphereSet():
    Diameter: list
    """ Diameter of the single scatterer in unit of meter. """
    Index: list = None
    """ Refractive index of scatterer. """
    Material: list = None
    """ Material of which the scatterer is made of. Only if Index is not specified. """
    nMedium: list = 1.0
    """ Refractive index of scatterer medium. """
    Name: str = 'sphere'
    """Name of the set """

    def __post_init__(self):
        self.BoundedIndex = True if self.Material is not None else False

        self.Diameter = XParameter(Values=ToList(self.Diameter, dtype=numpy.float64),
                                   Name='Diameter',
                                   Format=".2e",
                                   Unit="m",
                                   LongLabel='Diameter',
                                   Legend='Diameter',
                                   Type=numpy.float64)

        self.Material = XParameter(Values=ToList(self.Material, dtype=None),
                                   Name='Material',
                                   Format="",
                                   Unit="",
                                   LongLabel='Material',
                                   Legend='Material',
                                   Type=PyOptik.ExpData)

        self.Index = XParameter(Values=ToList(self.Index, dtype=numpy.complex128),
                                Name='Index',
                                Format="",
                                Unit="1",
                                LongLabel='Index',
                                Legend='Index',
                                Type=numpy.complex128)

        self.nMedium = XParameter(Values=ToList(self.nMedium, dtype=numpy.float64),
                                  Name='nMedium',
                                  LongLabel='nMedium',
                                  Format=".2f",
                                  Unit="1",
                                  Legend='nMedium',
                                  Type=numpy.float64)

    def BindToExperiment(self, Experiment):
        Experiment.Binding.set_sphere(self.Binding)

    def Evaluate(self, Source):
        if self.BoundedIndex:
            Material = numpy.asarray([material.GetRI(Source.Values) for material in self.Material])

            self.Binding = CppSphereSet(Diameter=self.Diameter.Values.astype(float),
                                        Material=Material.astype(complex),
                                        nMedium=self.nMedium.Values.astype(float))

        else:
            self.Binding = CppSphereSet(Diameter=self.Diameter.Values,
                                        Index=self.Index.Values,
                                        nMedium=self.nMedium.Values)

    def __append_to_table__(self, Table):
        if self.BoundedIndex:
            return [*Table, self.Diameter, self.Material, self.nMedium]

        else:
            return [*Table, self.Diameter, self.Index, self.nMedium]


@dataclass
class CylinderSet():
    Diameter: list
    """ Diameter of the single scatterer in unit of meter. """
    Index: list = None
    """ Refractive index of scatterer. """
    Material: list = None
    """ Refractive index of scatterer medium. """
    nMedium: list = 1.0
    """ Material of which the scatterer is made of. Only if Index is not specified. """
    Name: str = 'cylinder'
    """Name of the set """

    def __post_init__(self):
        self.BoundedIndex = True if self.Material is not None else False

        self.Diameter = XParameter(Values=ToList(self.Diameter, dtype=numpy.float64),
                                   Name='Diameter',
                                   Format=".2e",
                                   Unit="m",
                                   LongLabel='Diameter',
                                   Legend='Diameter',
                                   Type=numpy.float64)

        self.Material = XParameter(Values=ToList(self.Material, dtype=None),
                                   Name='Material',
                                   Format="",
                                   Unit="",
                                   LongLabel='Material',
                                   Legend='Material',
                                   Type=PyOptik.ExpData)

        self.Index = XParameter(Values=ToList(self.Index, dtype=numpy.complex128),
                                Name='Index',
                                Format="",
                                Unit="1",
                                LongLabel='Index',
                                Legend='Index',
                                Type=numpy.complex128)

        self.nMedium = XParameter(Values=ToList(self.nMedium, dtype=numpy.float64),
                                  Name='nMedium',
                                  LongLabel='nMedium',
                                  Format=".2f",
                                  Unit="1",
                                  Legend='nMedium',
                                  Type=numpy.float64)

    def BindToExperiment(self, Experiment):
        Experiment.Binding.set_cylinder(self.Binding)

    def Evaluate(self, Source):
        if self.BoundedIndex:
            Material = numpy.asarray([material.GetRI(Source.Values) for material in self.Material])

            self.Binding = CppCylinderSet(Diameter=self.Diameter.Values.astype(float),
                                          Material=Material.astype(complex),
                                          nMedium=self.nMedium.Values.astype(float))

        else:
            self.Binding = CppCylinderSet(Diameter=self.Diameter.Values,
                                          Index=self.Index.Values,
                                          nMedium=self.nMedium.Values)

    def __append_to_table__(self, Table):
        if self.BoundedIndex:
            return [*Table, self.Diameter, self.Material, self.nMedium]

        else:
            return [*Table, self.Diameter, self.Index, self.nMedium]


@dataclass
class SourceSet(object):
    Wavelength: float = 1.0
    """ Wavelenght of the light field. """
    Polarization: float = None
    """ Polarization of the light field in degree. """
    Amplitude: float = None
    """ Maximal value of the electric field at focus point. """
    Name: str = 'PlaneWave'
    """ Name of the set """

    def __post_init__(self):
        self.Polarization = LinearPolarization(self.Polarization)

        self.Wavelength = XParameter(Values=ToList(self.Wavelength, dtype=numpy.float64),
                                     Name='Wavelength',
                                     LongLabel='Wavelength',
                                     Format=".1e",
                                     Unit="m",
                                     Legend='Wavelength',
                                     Type=numpy.float64)

        self.Polarization = XParameter(Values=ToList(self.Polarization.Jones, dtype=numpy.complex128),
                                       Representation=ToList(self.Polarization.Angles, dtype=numpy.float64),
                                       Name='Polarization',
                                       LongLabel='Polarization',
                                       Format=".1f",
                                       Unit="Deg",
                                       Legend='Polarization',
                                       Type=numpy.float64)

        self.Amplitude = XParameter(Values=ToList(self.Amplitude, dtype=numpy.float64),
                                    Name='Amplitude',
                                    LongLabel='Amplitude',
                                    Format=".1e",
                                    Unit="w.m⁻¹",
                                    Legend='Amplitude',
                                    Type=numpy.float64)

        self.Binding = CppSourceSet(Wavelength=self.Wavelength.Values,
                                    Jones=self.Polarization.Values,
                                    Amplitude=self.Amplitude.Values)

    def BindToExperiment(self, Experiment):
        Experiment.Binding.set_source(self.Binding)

    def __append_to_table__(self, Table):
        return [*Table, self.Wavelength, self.Polarization, self.Amplitude]


@dataclass
class PhotodiodeSet():
    NA: list
    """ Numerical aperture of imaging system. """
    GammaOffset: list
    """ Angle [Degree] offset of detector in the direction perpendicular to polarization. """
    PhiOffset: list
    """ Angle [Degree] offset of detector in the direction parallel to polarization. """
    Filter: list
    """ Angle [Degree] of polarization filter in front of detector. """
    CouplingMode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    Coherent: bool = False
    """ Describe the detection scheme coherent or uncoherent. """
    Sampling: int = 200
    """ Describe the detection scheme coherent or uncoherent. """
    Name = "LPMode"
    """ Name of the set """

    def __post_init__(self):

        self.ScalarField = XParameter(Values=numpy.asarray([numpy.ones(self.Sampling)]),
                                      Representation=ToList('Photodiode', dtype=str),
                                      Name='Field',
                                      LongLabel='Coupling field',
                                      Format="",
                                      Unit="",
                                      Legend='C.F',
                                      Type=tuple)

        self.NA = XParameter(Values=ToList(self.NA, dtype=numpy.float64),
                             Name='NA',
                             LongLabel='Numerical aperture',
                             Format=".3f",
                             Unit="Rad",
                             Legend='NA',
                             Type=numpy.float64)

        self.PhiOffset = XParameter(Values=ToList(self.PhiOffset, dtype=numpy.float64),
                                    Name='PhiOffset',
                                    LongLabel='Phi offset',
                                    Format="03.1f",
                                    Unit="Deg",
                                    Legend='Phi offset',
                                    Type=numpy.float64)

        self.GammaOffset = XParameter(Values=ToList(self.GammaOffset, dtype=numpy.float64),
                                      Name='GammaOffset',
                                      LongLabel='Gamma offset',
                                      Format="03.1f",
                                      Unit="Deg",
                                      Legend='Gamma offset',
                                      Type=numpy.float64)

        self.Filter = XParameter(Values=ToList(self.Filter, dtype=numpy.float64),
                                 Name='Filter',
                                 LongLabel='Filter',
                                 Format="03.1f",
                                 Unit="Deg",
                                 Legend='Filter angle',
                                 Type=numpy.float64)

        self.__bind_to_cpp__()

    def __bind_to_cpp__(self):
        self.Binding = CppDetectorSet(ScalarField=self.ScalarField.Values,
                                      NA=self.NA.Values,
                                      PhiOffset=numpy.deg2rad(self.PhiOffset.Values),
                                      GammaOffset=numpy.deg2rad(self.GammaOffset.Values),
                                      Filter=numpy.array([x if x is not None else numpy.nan for x in self.Filter.Values]),
                                      PointCoupling=True if self.CouplingMode == 'Point' else False,
                                      Coherent=self.Coherent)

    def BindToExperiment(self, Experiment):
        Experiment.Binding.set_detector(self.Binding)

    def __append_to_table__(self, Table):
        return [*Table, self.ScalarField, self.NA, self.PhiOffset, self.GammaOffset, self.Filter]


@dataclass
class LPModeSet():
    Mode: list
    """ List of mode to be used. """
    NA: list
    """ Numerical aperture of imaging system. """
    GammaOffset: list
    """ Angle [Degree] offset of detector in the direction perpendicular to polarization. """
    PhiOffset: list
    """ Angle [Degree] offset of detector in the direction parallel to polarization. """
    Filter: list
    """ Angle [Degree] of polarization filter in front of detector. """
    CouplingMode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    Coherent: bool = False
    """ Describe the detection scheme coherent or uncoherent. """
    Sampling: int = 200
    """ Describe the detection scheme coherent or uncoherent. """
    Name = "LPMode"
    """ Name of the set """

    def __post_init__(self):

        self.ScalarField = XParameter(Values=numpy.asarray([LoadLPMode(ModeNumber=mode, Sampling=self.Sampling, Type='Unstructured') for mode in ToList(self.Mode)]),
                                      Representation=ToList(self.Mode, dtype=str),
                                      Name='Field',
                                      LongLabel='Coupling field',
                                      Format="",
                                      Unit="",
                                      Legend='C.F',
                                      Type=tuple)

        self.NA = XParameter(Values=ToList(self.NA, dtype=numpy.float64),
                             Name='NA',
                             LongLabel='Numerical aperture',
                             Format=".3f",
                             Unit="Rad",
                             Legend='NA',
                             Type=numpy.float64)

        self.PhiOffset = XParameter(Values=ToList(self.PhiOffset, dtype=numpy.float64),
                                    Name='PhiOffset',
                                    LongLabel='Phi offset',
                                    Format="03.1f",
                                    Unit="Deg",
                                    Legend='Phi offset',
                                    Type=numpy.float64)

        self.GammaOffset = XParameter(Values=ToList(self.GammaOffset, dtype=numpy.float64),
                                      Name='GammaOffset',
                                      LongLabel='Gamma offset',
                                      Format="03.1f",
                                      Unit="Deg",
                                      Legend='Gamma offset',
                                      Type=numpy.float64)

        self.Filter = XParameter(Values=ToList(self.Filter, dtype=numpy.float64),
                                 Name='Filter',
                                 LongLabel='Filter',
                                 Format="03.1f",
                                 Unit="Deg",
                                 Legend='Filter angle',
                                 Type=numpy.float64)

        self.__bind_to_cpp__()

    def __bind_to_cpp__(self):
        self.Binding = CppDetectorSet(ScalarField=self.ScalarField.Values,
                                      NA=self.NA.Values,
                                      PhiOffset=numpy.deg2rad(self.PhiOffset.Values),
                                      GammaOffset=numpy.deg2rad(self.GammaOffset.Values),
                                      Filter=numpy.array([x if x is not None else numpy.nan for x in self.Filter.Values]),
                                      PointCoupling=True if self.CouplingMode == 'Point' else False,
                                      Coherent=self.Coherent)

    def BindToExperiment(self, Experiment):
        Experiment.Binding.set_detector(self.Binding)

    def __append_to_table__(self, Table):
        return [*Table, self.ScalarField, self.NA, self.PhiOffset, self.GammaOffset, self.Filter]


class Setup(object):
    def __init__(self, ScattererSet=None, SourceSet=None, DetectorSet=None):

        self.SourceSet = SourceSet

        self.DetectorSet = DetectorSet

        self.ScattererSet = ScattererSet

        self.ScattererSet.Evaluate(self.SourceSet.Wavelength)

        self.Binding = CppExperiment()

        self.BindElements()

        self.Xtable = self.SourceSet.__append_to_table__([])
        self.Xtable = self.ScattererSet.__append_to_table__(self.Xtable)

        if self.DetectorSet is not None:
            self.Xtable = self.DetectorSet.__append_to_table__(self.Xtable)

    def BindElements(self):
        self.SourceSet.BindToExperiment(self)
        self.ScattererSet.BindToExperiment(self)

        if self.DetectorSet:
            self.DetectorSet.BindToExperiment(self)

    def Get(self, Input: list) -> DataV:
        """Methode generate array of the givens parameters as a function of
        all independent variables.

        """

        Input = ToList(Input)

        self.Ytable = Input

        Array = []
        for prop in Input:
            prop.Values = numpy.array([])

            prop = 'get' + "_" + self.ScattererSet.Name + "_" + prop.Name

            Array.append(getattr(self.Binding, prop)())

        Array = numpy.asarray(Array)

        for n, e in enumerate(self.Xtable):
            e.Position = n + 1

        return DataV(Array, Xtable=self.Xtable, Ytable=self.Ytable)
