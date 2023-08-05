#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import logging
from dataclasses import dataclass

from PyOptik import ExpData
from PyMieSim.Tools.Mesh import FibonacciMesh
from PyMieSim.Source import PlaneWave
from PyMieSim.Tools.Constants import c, epsilon0
from PyMieSim.Tools.Representations import S1S2, FarField, Stokes, SPF


class GenericScatterer():
    """
    .. note::

        Generic class for scatterer

    """

    @property
    def SizeParameter(self):
        return self.Bind.SizeParameter

    @property
    def Area(self):
        return self.Bind.Area

    @property
    def Qsca(self):
        """ Scattering efficiency. """
        return self.Bind.Qsca

    @property
    def Qext(self):
        """ Extinction efficiency. """
        return self.Bind.Qext

    @property
    def Qabs(self):
        """ Absorption efficiency. """
        return self.Bind.Qabs

    @property
    def Qback(self):
        """ Backscattering efficiency. """
        return self.Bind.Qback

    @property
    def Qratio(self):
        """ Efficiency: Ratio of backscattering over total scattering. """
        return self.Bind.Qratio

    @property
    def g(self):
        """ Anisotropy factor. """
        return self.Bind.g

    @property
    def Qpr(self):
        """ Radiation pressure efficiency. """
        return self.Bind.Qpr

    @property
    def Csca(self):
        """ Scattering cross-section. """
        return (self.Bind.Csca)

    @property
    def Cext(self):
        """ Extinction cross-section. """
        return (self.Bind.Cext)

    @property
    def Cabs(self):
        """ Absorption cross-section. """
        return (self.Bind.Cabs)

    @property
    def Cpr(self):
        """ Radiation pressure cross-section. """
        return (self.Bind.Cpr)

    @property
    def Cback(self):
        """ Backscattering cross-section. """
        return (self.Bind.Cback)

    @property
    def Cratio(self):
        """ Ratio of backscattering cross-section over total scattering. """
        return (self.Bind.Cratio)

    def _FarField(self, Phi, Theta, R, Structured: bool = False) -> numpy.array:
        r"""
        .. note::

            Method Compute scattering Far Field for unstructured coordinate.

            .. math::
                \text{Fields} = E_{||}(\phi,\theta),
                                 E_{\perp}(\phi,\theta)


            The Fields are up to a constant phase value.

            .. math::
                \exp{\big(-i k r \big)}


        Parameters:
            Num : Number of point to spatially (:math:`\phi , \theta`) evaluate the Fields [Num, Num].


        """

        if Structured:
            return self.Bind.FullFields(Phi.size, R=R)
        else:
            return self.Bind.Fields(Phi=Phi, Theta=Theta, R=R)

    def S1S2(self, **kwargs) -> S1S2:
        r"""
        .. note::

            Method compute :math:`S_1(\phi)` and :math:`S_2(\phi)`.
            For spherical Scatterer such as here S1 and S2 are computed as follow:

            .. math::
                S_1=\sum\limits_{n=1}^{n_{max}} \frac{2n+1}{n(n+1)}(a_n \pi_n+b_n \tau_n)

                .

                S_2=\sum\limits_{n=1}^{n_{max}}\frac{2n+1}{n(n+1)}(a_n \tau_n+b_n \pi_n)

        Parameters:
            Num :  Number of point to define (:math:`\phi`) angle to evaluate :math:`S_1` and :math:`S_2`.
            Phi :  List of angle (:math:`\phi`) to evaluate :math:`S_1` and :math:`S_2`. Only if Num is not specified.

        """

        return S1S2(Parent=self, **kwargs)

    def Stokes(self, **kwargs) -> Stokes:
        r"""
        .. note::

            Method compute and return the Stokes parameters: I, Q, U, V.
            Those parameters are defined as:

            .. math:
                I &= \big| E_x \big|^2 + \big| E_y \big|^2

                Q &= \big| E_x \big|^2 - \big| E_y \big|^2

                U &= 2 \mathcal{Re} \big\{ E_x E_y^* \big\}

                V &= 2 \mathcal{Im} \big\{ E_x E_y^* \big\}

        Parameters:
            Num : Number of point for the mesh to evaluate the stokes parameters [Num x Num]

        """

        return Stokes(Parent=self, **kwargs)

    def FarField(self, **kwargs) -> FarField:
        r"""
        .. note::

            Method Compute scattering Far Field.

            .. math::
                \text{Fields} = E_{||}(\phi,\theta)^2,
                                 E_{\perp}(\phi,\theta)^2


            The Fields are up to a constant phase value:

            .. math::
                \exp{\big(-i k r \big)}

        Parameters:
            Num : Number of point to spatially (:math:`\phi , \theta`) evaluate the Fields [Num, Num].



        """

        return FarField(Parent=self, **kwargs)

    def SPF(self, **kwargs) -> SPF:
        r"""
        .. note::

            Scattering phase function.

            .. math::
                \text{SPF} = \sqrt{ E_{\parallel}(\phi,\theta)^2
                + E_{\perp}(\phi,\theta)^2 }

        Parameters :
            Num : Number of point to spatially (:math:`\theta , \phi`) evaluate the SPF [Num, Num].


        """

        return SPF(Parent=self, **kwargs)

    def PoyntingVector(self, Mesh: FibonacciMesh) -> float:
        r"""
        .. note::

            Method return the Poynting vector norm defined as:

            .. math::
                \vec{S} = \epsilon c^2 \vec{E} \times \vec{B}

        Parameters :
            Mesh : Number of voxel in the 4 pi space to compute energy flow.

        """

        EPhi, ETheta = self._FarField(Mesh.Phi.Radian, Mesh.Theta.Radian, 1., Structured=False)

        NormE = numpy.sqrt(numpy.abs(EPhi)**2 + numpy.abs(ETheta)**2)

        NormB = NormE / c

        Poynting = epsilon0 * c**2 * NormE * NormB

        return Poynting

    def EnergyFlow(self, Mesh: FibonacciMesh) -> float:
        r"""
        .. note::

            Method return energy flow defined as:

            .. math::

                W_a &= \sigma_{sca} * I_{inc}

                .

                P &= \int_{A} I dA

                .

                I &= \frac{c n \epsilon_0}{2} |E|^2

            | With:
            |     I : Energy density
            |     n  : Refractive index of the medium
            |     :math:`\epsilon_0` : Vaccum permitivity
            |     E  : Electric field
            |     \sigma_{sca}: Scattering cross section.

            More info on wikipedia link (see ref[6]).


        Parameters :
            Mesh : Number of voxel in the 4 pi space to compute energy flow.

        Returns
        -------
        :class:`float`
            Energy flow [:math:`W`]

        """

        Poynting = self.PoyntingVector(Mesh)

        if Mesh.Structured:
            Wtotal = 0.5 * numpy.sum(Poynting * Mesh.SinMesh) * Mesh.dOmega.Radian

        else:
            Wtotal = 0.5 * numpy.sum(Poynting) * Mesh.dOmega.Radian

        return Wtotal

    def CrossSection(self, Mesh: FibonacciMesh):
        r"""
        .. note::

            Method return scattering cross section, see :func:`EnergyFlow`

        Parameters :
            Mesh : Number of voxel in the 4 pi space to compute scattering cross section.

        """

        return (self.Qsca * self.Area)  # similar to self.EnergyFlow(Mesh) / self.Source.I

    def AssignIndexOrMaterial(self, Index, Material):
        assert bool(Index) ^ bool(Material), logging.error("Exactly one of the parameter [Index or Material] have to be assigned.")
        Index = Index if Index is not None else Material.GetRI(self.Source.Wavelength)
        Material = Material if Material is not None else None
        return Index, Material


@dataclass()
class Sphere(GenericScatterer):
    r"""
    .. note::

        Class representing a homogeneous spherical scatterer.
    """

    Diameter: float
    """ Diameter of the single scatterer in unit of meter. """
    Source: PlaneWave
    """ Light source object containing info on polarization and wavelength. """
    Index: complex = None
    """ Refractive index of scatterer. """
    nMedium: float = 1.0
    """ Refractive index of scatterer medium. """
    Material: ExpData = None
    """ Material of which the scatterer is made of. Only if Index is not specified. """

    def __post_init__(self):
        self.Index, self.Material = self.AssignIndexOrMaterial(self.Index, self.Material)

        self.GetBinding()

    def GetBinding(self) -> None:
        r"""
        .. note::

            Method call and bind c++ scatterer class

        """
        from PyMieSim.bin.SphereInterface import SPHERE

        self.Bind = SPHERE(Wavelength=self.Source.Wavelength,
                           Amplitude=self.Source.Amplitude,
                           Diameter=self.Diameter,
                           Index=self.Index,
                           nMedium=self.nMedium,
                           Jones=self.Source.Polarization.Jones.squeeze())

    def an(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::

            Compute :math:`a_n` coefficient as defined in Eq:III.88 of B&B:

            .. math::
                a_n = \frac{
                \mu_{sp} \Psi_n(\alpha) \Psi_n^\prime(\beta) -
                \mu M \Psi_n^\prime(\alpha) \Psi_n(\beta)}
                {\mu_{sp} \xi_n(\alpha) \Psi_n^\prime(\beta)-
                \mu M \xi_n^\prime (\alpha) \Psi_n(\beta)}

            With :math:`M = \frac{k_{sp}}{k}` (Eq:I.103)

        """
        return self.Bind.an()

    def bn(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::

            Compute :math:`b_n` coefficient as defined in Eq:III.89 of B&B:

            .. math::
                b_n = \frac{
                \mu M \Psi_n(\alpha) \Psi_n^\prime(\beta) -
                \mu_{sp} \Psi_n^\prime(\alpha) \Psi_n(\beta)}
                {\mu M \xi_n(\alpha) \Psi_n^\prime(\beta)-
                \mu_{sp} \xi_n^\prime (\alpha) \Psi_n(\beta)}

            With :math:`M = \frac{k_{sp}}{k}` (Eq:I.103)

        """
        return self.Bind.bn()

    def cn(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::
            Compute :math:`c_n` coefficient as defined in Eq:III.90 of B&B:

            .. math::
                c_n = \frac{
                \mu_{sp} M \big[ \xi_n(\alpha) \Psi_n^\prime(\alpha) -
                \xi_n^\prime(\alpha) \Psi_n(\alpha) \big]}
                {\mu_{sp} \xi_n(\alpha) \Psi_n^\prime(\beta)-
                \mu M \xi_n^\prime (\alpha) \Psi_n(\beta)}

            With :math:`M = \frac{k_{sp}}{k}` (Eq:I.103)

        """
        return self.Bind.cn()

    def dn(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::

            Compute :math:`d_n` coefficient as defined in Eq:III.91 of B&B:

            .. math::
                d_n = \frac{
                \mu M^2 \big[ \xi_n(\alpha) \Psi_n^\prime(\alpha) -
                \xi_n^\prime(\alpha) \Psi_n(\alpha) \big]}
                {\mu M \xi_n(\alpha) \Psi_n^\prime(\beta)-
                \mu_{sp} M \xi_n^\prime (\alpha) \Psi_n(\beta)}

            With :math:`M = \frac{k_{sp}}{k}` (Eq:I.103)

        """
        return self.Bind.dn()


@dataclass()
class CoreShell(GenericScatterer):
    r"""
    .. note::
        Class representing a core+shell spherical scatterer.

    """

    CoreDiameter: float
    """ Diameter of the core of the single scatterer [m]. """
    ShellWidth: float
    """ Diameter of the shell of the single scatterer [m]. """
    Source: PlaneWave
    """ Light source object containing info on polarization and wavelength. """
    CoreIndex: complex = None
    """ Refractive index of the core of the scatterer. """
    ShellIndex: complex = None
    """ Refractive index of the shell of the scatterer. """
    CoreMaterial: ExpData = None
    """ Core material of which the scatterer is made of. Only if CoreIndex is not specified.  """
    ShellMaterial: ExpData = None
    """ Shell material of which the scatterer is made of. Only if ShellIndex is not specified.  """
    nMedium: float = 1.0
    """ Refractive index of scatterer medium. """

    def __post_init__(self):

        self.CoreIndex, self.CoreMaterial = self.AssignIndexOrMaterial(self.CoreIndex, self.CoreMaterial)
        self.ShellIndex, self.ShellMaterial = self.AssignIndexOrMaterial(self.ShellIndex, self.ShellMaterial)

        self.ShellDiameter = self.CoreDiameter + self.ShellWidth

        self.GetBinding()

    def GetBinding(self) -> None:
        r"""
        .. note::
            Method call and bind c++ scatterer class
        """
        from PyMieSim.bin.CoreShellInterface import CORESHELL

        self.Bind = CORESHELL(ShellIndex=self.ShellIndex,
                              CoreIndex=self.CoreIndex,
                              ShellDiameter=self.ShellDiameter,
                              CoreDiameter=self.CoreDiameter,
                              Wavelength=self.Source.Wavelength,
                              nMedium=self.nMedium,
                              Jones=self.Source.Polarization.Jones.squeeze(),
                              Amplitude=self.Source.Amplitude)

    def an(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::
            Compute :math:`a_n` coefficient

        """
        if MaxOrder is None:
            return self.Bind.an()
        else:
            return self.Bind._an(MaxOrder)

    def bn(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::
            Compute :math:`b_n` coefficient.

        """
        if MaxOrder is None:
            return self.Bind.bn()
        else:
            return self.Bind._bn(MaxOrder)


@dataclass()
class Cylinder(GenericScatterer):
    r"""
    .. note::
        Class representing a right angle cylindrical scatterer.
    """

    Diameter: float
    """ Diameter of the single scatterer in unit of meter. """
    Source: PlaneWave
    """ Light source object containing info on polarization and wavelength. """
    Index: complex = None
    """ Refractive index of scatterer. """
    nMedium: float = 1.0
    """ Material of which the scatterer is made of. Only if Index is not specified. """
    Material: ExpData = None
    """ Refractive index of scatterer medium. """

    def __post_init__(self):
        self.Index, self.Material = self.AssignIndexOrMaterial(self.Index, self.Material)

        self.GetBinding()

    def GetBinding(self) -> None:
        r"""
        .. note::

            Method call and bind c++ scatterer class

        """
        from PyMieSim.bin.CylinderInterface import CYLINDER

        self.Bind = CYLINDER(Index=self.Index,
                             Diameter=self.Diameter,
                             Wavelength=self.Source.Wavelength,
                             nMedium=self.nMedium,
                             Amplitude=self.Source.Amplitude,
                             Jones=self.Source.Polarization.Jones.squeeze())

    def a1n(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::
            Compute :math:`a_n` coefficient as defined ref[5]:

            .. math::
                a_n = \frac{ m_t J_n(m_t x) J_n^\prime (m x) - m J_n^\prime (m_t x) J_n(m x) }
                { m_t J_n(m_t x) H_n^\prime (m x) - m J_n^\prime (m_t x) H_n(m x) }

            | With :math:`m` being the refractive index of the medium and
            |      :math:`m_t` being the refractive index of the index.

        """

        return self.Bind.a1n()

    def a2n(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::
            Compute :math:`a_n` coefficient as defined ref[5]:

            .. math::
                a_n = \frac{ m_t J_n(m_t x) J_n^\prime (m x) - m J_n^\prime (m_t x) J_n(m x) }
                { m_t J_n(m_t x) H_n^\prime (m x) - m J_n^\prime (m_t x) H_n(m x) }

            | With :math:`m` being the refractive index of the medium and
            |      :math:`m_t` being the refractive index of the index.

        """

        return self.Bind.a2n()

    def b1n(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::
            Compute :math:`b_n` coefficient as defined in ref[5]:

            .. math::
                b_n = \frac{ m J_n(m_t x) J_n^\prime (m x) - m_t J_n^\prime (m_t x) J_n(m x) }
                { m J_n(m_t x) H_n^\prime (m x) - m_t J_n^\prime (m_t x) H_n(m x) }

            | With :math:`m` being the refractive index of the medium and
            |      :math:`m_t` being the refractive index of the index.

        """

        return self.Bind.b1n()

    def b2n(self, MaxOrder: int = None) -> numpy.array:
        r"""
        .. note::
            Compute :math:`b_n` coefficient as defined in ref[5]:

            .. math::
                b_n = \frac{ m J_n(m_t x) J_n^\prime (m x) - m_t J_n^\prime (m_t x) J_n(m x) }
                { m J_n(m_t x) H_n^\prime (m x) - m_t J_n^\prime (m_t x) H_n(m x) }

            | With :math:`m` being the refractive index of the medium and
            |      :math:`m_t` being the refractive index of the index.

        """

        return self.Bind.b2n()

# -
