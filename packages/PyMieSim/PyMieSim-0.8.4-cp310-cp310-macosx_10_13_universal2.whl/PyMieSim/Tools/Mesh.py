#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
from dataclasses import dataclass

from PyMieSim.bin.Fibonacci import FIBONACCI
from MPSPlots.Render3D import Scene3D
from MPSPlots.Math import Angle


@dataclass
class FibonacciMesh():
    """
    Class wich represent an angular mesh. The distribution of points inside
    the mesh is similar to a Fibonacci sphere where each point cover an
    equivalent solid angle.

    """

    MaxAngle: float = 1.5
    """ Angle in radian defined by the numerical aperture of the imaging system. """
    Sampling: int = 1000
    """Number of point distrubuted inside the Solid angle defined by the numerical aperture. """
    PhiOffset: float = 0.
    """ Angle offset in the parallel direction of the polarization of incindent light. """
    GammaOffset: float = 0.
    """ Angle offset in the perpendicular direction of the polarization of incindent light. """

    def __post_init__(self):
        self.Structured = False

        self._Para = None
        self._Perp = None

        self._ParaPlan = None
        self._PerpPlan = None

        self._VPerp = None
        self._HPerp = None
        self._VPara = None
        self._HPara = None

        self._Phi = None
        self._Theta = None

        self._Plan = None

        self.VVec = numpy.array([1, 0, 0])
        self.HVec = numpy.array([0, 1, 0])
        self.GenerateLedevedMesh()

    @property
    def Plan(self):
        if self._Plan is None:
            self.Binding.ComputePlan()
            self._Plan = numpy.asarray([self.Binding.XPlan, self.Binding.YPlan, self.Binding.ZPlan])
            return self._Plan
        else:
            return self._Plan

    @property
    def Perp(self):
        if self._Perp is None:
            self.Binding.ComputeVectorField()
            self._Para, self._Perp = self.Binding.ParaVector, self.Binding.PerpVector
            return self._Perp
        else:
            return self._Perp

    @property
    def Para(self):
        if self._Para is None:
            self.Binding.ComputeVectorField()
            self._Para, self._Perp = self.Binding.ParaVector, self.Binding.PerpVector
            return self._Para
        else:
            return self._Para

    @property
    def HPerp(self):
        if self._HPerp is None:
            self.Binding.ComputeVectorField()
            self._HPerp = self.Binding.HPerpVector
            return self._HPerp
        else:
            return self._HPerp

    @property
    def HPara(self):
        if self._HPara is None:
            self.Binding.ComputeVectorField()
            self._HPara = self.Binding.HParaVector
            return self._HPara
        else:
            return self._HPara

    @property
    def VPerp(self):
        if self._VPerp is None:
            self.Binding.ComputeVectorField()
            self._VPara, self._VPerp = self.Binding.ParaVector, self.Binding.PerpVector
            return self._VPerp
        else:
            return self._VPerp

    @property
    def VPara(self):
        if self._VPara is None:
            self.Binding.ComputeVectorField()
            self._VPara, self._VPerp = self.Binding.ParaVector, self.Binding.PerpVector
            return self._VPara
        else:
            return self._VPara

    @property
    def ParaPlan(self):
        if self._ParaPlan is None:
            self.Binding.ComputeVectorField()
            self._ParaPlan = self.Binding.ParaVectorZPlanar
            self._PerpPlan = self.Binding.PerpVectorZPlanar
            return self._ParaPlan
        else:
            return self._ParaPlan

    @property
    def PerpPlan(self):
        if self._PerpPlan is None:
            self.Binding.ComputeVectorField()
            self._ParaPlan = self.Binding.ParaVectorZPlanar
            self._PerpPlan = self.Binding.PerpVectorZPlanar
            return self._PerpPlan
        else:
            return self._PerpPlan

    @property
    def Phi(self):
        if not self._Phi:
            self._Phi = Angle(self.Binding.Phi, Unit='Radian')
            return self._Phi
        else:
            return self._Phi

    @property
    def Theta(self):
        if not self._Theta:
            self._Theta = Angle(self.Binding.Theta, Unit='Radian')
            return self._Theta
        else:
            return self._Theta

    @property
    def X(self):
        return self.Binding.X

    @property
    def Y(self):
        return self.Binding.Y

    @property
    def Z(self):
        return self.Binding.Z

    def MakeProperties(self):

        self.CartMesh = numpy.asarray([self.Binding.X, self.Binding.Y, self.Binding.Z])

        self.dOmega = Angle(0, Unit='Radian')
        self.dOmega.Radian = self.Binding.dOmega
        self.dOmega.Degree = self.Binding.dOmega * (180 / numpy.pi)**2

        self.Omega = Angle(0, Unit='Radian')
        self.Omega.Radian = self.Binding.Omega
        self.Omega.Degree = self.Binding.Omega * (180 / numpy.pi)**2

    def ProjectionHVVector(self):
        ParaProj = numpy.array([self.ProjectionOnBaseVector(Vector=self.VParaPlan, BaseVector=X) for X in [self.VVec, self.HVec]])

        PerpProj = numpy.array([self.ProjectionOnBaseVector(Vector=self.VPerpPlan, BaseVector=X) for X in [self.VVec, self.HVec]])

        return ParaProj, PerpProj

    def ProjectionHVScalar(self):
        ParaProj = numpy.array([self.ProjectionOnBaseScalar(Vector=self.VParaZPlan, BaseVector=X) for X in [self.VVec, self.HVec]])

        PerpProj = numpy.array([self.ProjectionOnBaseScalar(Vector=self.VPerpZPlan, BaseVector=X) for X in [self.VVec, self.HVec]])

        return ParaProj, PerpProj

    def ProjectionOnBaseScalar(self, Vector, BaseVector):
        return Vector.dot(BaseVector)

    def ProjectionOnBaseVector(self, Vector, BaseVector):
        proj = self.ProjectionOnBaseScalar(Vector, BaseVector)

        OutputVector = numpy.outer(proj, BaseVector)

        return OutputVector

    def Plot(self):
        figure = Scene3D(shape=(1, 1))
        self.__plot__add_mesh__(figure=figure, plot_number=(0, 0))

        return figure

    def __plot__add_mesh__(self, figure, plot_number: tuple):
        Coordinate = numpy.array([self.X, self.Y, self.Z])

        figure.Add_Unstructured(Plot=plot_number,
                                Coordinate=Coordinate,
                                color="k")

        figure.__add_unit_sphere__(Plot=plot_number)
        figure.__add_axes__(Plot=plot_number)
        figure.__add__text__(Plot=plot_number, Text='Mesh grid')

    def GenerateLedevedMesh(self):
        self.Binding = FIBONACCI(self.Sampling,
                             self.MaxAngle,
                             numpy.deg2rad(self.PhiOffset),
                             numpy.deg2rad(self.GammaOffset))

        self.MakeProperties()


# -
