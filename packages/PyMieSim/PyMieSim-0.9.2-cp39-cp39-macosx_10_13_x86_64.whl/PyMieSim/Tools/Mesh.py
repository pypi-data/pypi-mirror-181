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

    max_angle: float = 1.5
    """ Angle in radian defined by the numerical aperture of the imaging system. """
    sampling: int = 1000
    """Number of point distrubuted inside the Solid angle defined by the numerical aperture. """
    phi_offset: float = 0.
    """ Angle offset in the parallel direction of the polarization of incindent light. """
    gamma_offset: float = 0.
    """ Angle offset in the perpendicular direction of the polarization of incindent light. """

    def __post_init__(self):
        self.structured = False

        self._para = None
        self._perp = None

        self._para_plan = None
        self._perp_plan = None

        self._Vperp = None
        self._Hperp = None
        self._Vpara = None
        self._Hpara = None

        self._phi = None
        self._theta = None

        self._plan = None

        self.VVec = numpy.array([1, 0, 0])
        self.HVec = numpy.array([0, 1, 0])
        self.generate_ledeved_mesh()

    @property
    def plan(self):
        if self._plan is None:
            self.Binding.Computeplan()
            self._plan = numpy.asarray([self.Binding.Xplan, self.Binding.Yplan, self.Binding.Zplan])
            return self._plan
        else:
            return self._plan

    @property
    def perp(self):
        if self._perp is None:
            self.Binding.ComputeVectorField()
            self._para, self._perp = self.Binding.paraVector, self.Binding.perpVector
            return self._perp
        else:
            return self._perp

    @property
    def para(self):
        if self._para is None:
            self.Binding.ComputeVectorField()
            self._para, self._perp = self.Binding.paraVector, self.Binding.perpVector
            return self._para
        else:
            return self._para

    @property
    def Hperp(self):
        if self._Hperp is None:
            self.Binding.ComputeVectorField()
            self._Hperp = self.Binding.HperpVector
            return self._Hperp
        else:
            return self._Hperp

    @property
    def Hpara(self):
        if self._Hpara is None:
            self.Binding.ComputeVectorField()
            self._Hpara = self.Binding.HparaVector
            return self._Hpara
        else:
            return self._Hpara

    @property
    def Vperp(self):
        if self._Vperp is None:
            self.Binding.ComputeVectorField()
            self._Vpara, self._Vperp = self.Binding.paraVector, self.Binding.perpVector
            return self._Vperp
        else:
            return self._Vperp

    @property
    def Vpara(self):
        if self._Vpara is None:
            self.Binding.ComputeVectorField()
            self._Vpara, self._Vperp = self.Binding.paraVector, self.Binding.perpVector
            return self._Vpara
        else:
            return self._Vpara

    @property
    def para_plan(self):
        if self._para_plan is None:
            self.Binding.ComputeVectorField()
            self._para_plan = self.Binding.paraVectorZplanar
            self._perp_plan = self.Binding.perpVectorZplanar
            return self._para_plan
        else:
            return self._para_plan

    @property
    def perp_plan(self):
        if self._perp_plan is None:
            self.Binding.ComputeVectorField()
            self._para_plan = self.Binding.paraVectorZplanar
            self._perp_plan = self.Binding.perpVectorZplanar
            return self._perp_plan
        else:
            return self._perp_plan

    @property
    def phi(self):
        if not self._phi:
            self._phi = Angle(self.Binding.phi, Unit='Radian')
            return self._phi
        else:
            return self._phi

    @property
    def theta(self):
        if not self._theta:
            self._theta = Angle(self.Binding.theta, Unit='Radian')
            return self._theta
        else:
            return self._theta

    @property
    def X(self):
        return self.Binding.x

    @property
    def Y(self):
        return self.Binding.y

    @property
    def Z(self):
        return self.Binding.z

    def _make_properties_(self):

        self.CartMesh = numpy.asarray([self.Binding.x, self.Binding.y, self.Binding.z])

        self.d_omega = Angle(0, Unit='Radian')
        self.d_omega.Radian = self.Binding.d_omega
        self.d_omega.Degree = self.Binding.d_omega * (180 / numpy.pi)**2

        self.omega = Angle(0, Unit='Radian')
        self.omega.Radian = self.Binding.omega
        self.omega.Degree = self.Binding.omega * (180 / numpy.pi)**2

    def projection_HV_vector(self):
        paraProj = numpy.array([self.projection_on_base_vector(Vector=self.Vpara_plan, BaseVector=X) for X in [self.VVec, self.HVec]])

        perpProj = numpy.array([self.projection_on_base_vector(Vector=self.Vperp_plan, BaseVector=X) for X in [self.VVec, self.HVec]])

        return paraProj, perpProj

    def projection_HV_scalar(self):
        paraProj = numpy.array([self.projection_on_base_scalar(Vector=self.VparaZplan, BaseVector=X) for X in [self.VVec, self.HVec]])

        perpProj = numpy.array([self.projection_on_base_scalar(Vector=self.VperpZplan, BaseVector=X) for X in [self.VVec, self.HVec]])

        return paraProj, perpProj

    def projection_on_base_scalar(self, Vector, BaseVector):
        return Vector.dot(BaseVector)

    def projection_on_base_vector(self, Vector, BaseVector):
        proj = self.projection_on_base_scalar(Vector, BaseVector)

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

    def generate_ledeved_mesh(self):
        self.Binding = FIBONACCI(self.sampling,
                             self.max_angle,
                             numpy.deg2rad(self.phi_offset),
                             numpy.deg2rad(self.gamma_offset))

        self._make_properties_()


# -
