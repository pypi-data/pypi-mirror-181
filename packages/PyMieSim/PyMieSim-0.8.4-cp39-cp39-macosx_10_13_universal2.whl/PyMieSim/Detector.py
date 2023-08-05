#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import logging
from dataclasses import dataclass

from PyMieSim.Tools.Representations import Footprint
from PyMieSim.Tools.Mesh import FibonacciMesh
from MPSPlots.Math import NA2Angle
from PyMieSim.bin.DetectorInterface import BindedDetector
from PyMieSim import LoadLPMode
from MPSPlots.Render3D import Scene3D


@dataclass
class GenericDetector():
    r"""
    .. note::
        Detector type class representing a photodiode, light coupling is
        thus independant of the phase of the latter.
    """

    ScalarField: numpy.ndarray
    """ Array representing the detection field distribution. """
    NA: float
    """ Numerical aperture of imaging system. """
    GammaOffset: float
    """ Angle [Degree] offset of detector in the direction perpendicular to polarization. """
    PhiOffset: float
    """ Angle [Degree] offset of detector in the direction parallel to polarization. """
    Filter: float
    """ Angle [Degree] of polarization filter in front of detector. """
    CouplingMode: str = 'Point'
    """ Method for computing mode coupling. Either Point or Mean. """
    Coherent: bool = False
    """ Describe the detection scheme coherent or uncoherent. """

    def __post_init__(self):
        self.Sampling = self.ScalarField.size
        self.MaxAngle = NA2Angle(self.NA)
        self.Mesh = FibonacciMesh(MaxAngle=self.MaxAngle,
                                  Sampling=self.Sampling,
                                  PhiOffset=self.PhiOffset,
                                  GammaOffset=self.GammaOffset)

    def GetBinding(self):
        self.Bind = BindedDetector(ScalarField=self.ScalarField,
                                   NA=self.NA,
                                   PhiOffset=numpy.deg2rad(self.PhiOffset),
                                   GammaOffset=numpy.deg2rad(self.GammaOffset),
                                   Filter=numpy.nan if self.Filter is None else numpy.deg2rad(self.Filter),
                                   Coherent=self.Coherent,
                                   PointCoupling=True if self.CouplingMode == 'PointCoupling' else False
                                   )

    def GetStructuredScalarField(self):
        return numpy.ones([self.Sampling, self.Sampling])

    def Coupling(self, Scatterer):
        r"""
        .. note::
            Return the value of the scattererd light coupling as computed as:

            .. math::
                |\iint_{\Omega}  \Phi_{det} \,\, \Psi_{scat}^* \,  d \Omega|^2

            | Where:
            |   :math:`\Phi_{det}` is the capturing field of the detector and
            |   :math:`\Psi_{scat}` is the scattered field.

        Parameters
        ----------
        Scatterer : :class:`Scatterer`
            Scatterer instance (sphere, cylinder, ...).

        Returns
        -------
        :class:`float`
            Value of the coupling.

        """

        return getattr(self.Bind, "Coupling" + type(Scatterer).__name__)(Scatterer.Bind)

    def Footprint(self, Scatterer):
        r"""
        .. note::
            Return the footprint of the scattererd light coupling with the
            detector as computed as:

            .. math::
                \big| \mathscr{F}^{-1} \big\{ \tilde{ \psi } (\xi, \nu),\
                       \tilde{ \phi}_{l,m}(\xi, \nu)  \big\}
                       (\delta_x, \delta_y) \big|^2

            | Where:
            |   :math:`\Phi_{det}` is the capturing field of the detector and
            |   :math:`\Psi_{scat}` is the scattered field.

        Parameters
        ----------
        Scatterer : :class:`Scatterer`.
            Scatterer instance (sphere, cylinder, ...).

        Returns
        -------
        :class:`Footprint`.
            Dictionnary subclass with all pertienent information.

        """
        return Footprint(Scatterer=Scatterer, Detector=self)

    def Plot(self):
        r"""
        .. note::
            Method that plot the real part of the scattered field
            (:math:`E_{\theta}` and :math:`E_{\phi}`).

        """
        Coordinate = numpy.array([self.Mesh.X, self.Mesh.Y, self.Mesh.Z])

        figure = Scene3D(shape=(1, 2), window_size=[1800, 1000])

        for Plot, Scalar, Name in zip([(0, 0), (0, 1)],
                                      [self.ScalarField.real, self.ScalarField.imag],
                                      ['Real', 'Imaginary']):

            figure.Add_Unstructured(Plot=Plot,
                                    Coordinate=Coordinate,
                                    Scalar=Scalar,
                                    color="tan",
                                    scalar_bar_args={'title': f'{Name} field'}
                                    )

            figure.__add_unit_sphere__(Plot=Plot)
            figure.__add_axes__(Plot=Plot)
            # figure.__add__text__(Plot=Plot, Text=f'{Name} part')

        return figure


class Photodiode(GenericDetector):
    Description = "[Photodiode]"

    def __init__(self, NA, Sampling, GammaOffset, PhiOffset, Filter=None):

        super().__init__(ScalarField=numpy.ones(Sampling).astype(complex),
                         NA=NA,
                         PhiOffset=PhiOffset,
                         GammaOffset=GammaOffset,
                         Filter=Filter,
                         Coherent=False,
                         CouplingMode='Point')

        self.GetBinding()


class IntegratingSphere(GenericDetector):
    Description = "[Integration sphere]"

    def __init__(self, Sampling, Filter=None):

        super().__init__(ScalarField=numpy.ones(Sampling).astype(complex),
                         NA=2,
                         PhiOffset=0,
                         GammaOffset=0,
                         Filter=Filter,
                         Coherent=False,
                         CouplingMode='Point')

        self.GetBinding()


class LPmode(GenericDetector):
    Description = "[LP mode detector]"

    def __init__(self,
                 Mode: list,
                 NA: float,
                 GammaOffset: float,
                 PhiOffset: float,
                 Sampling: int = 200,
                 Rotation: float = 0,
                 Filter: float = None,
                 CouplingMode: str = 'Point'):

        if NA > 0.3 or NA < 0:
            logging.warning("High values of NA do not comply with paraxial approximation. Value under 0.3 are prefered.")

        self.Mode = Mode

        super().__init__(ScalarField=LoadLPMode(self.Mode, Type='Unstructured', Sampling=Sampling).astype(complex),
                         NA=NA,
                         PhiOffset=PhiOffset,
                         GammaOffset=GammaOffset,
                         Filter=Filter,
                         Coherent=True,
                         CouplingMode=CouplingMode)

        self.GetBinding()

    def GetStructuredScalarField(self):
        return LoadLPMode(self.Mode, Type='Structured').astype(complex),


# -
