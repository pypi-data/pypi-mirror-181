#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

import PyMieSim
from MPSPlots.Render3D import Scene3D
import MPSPlots.Render2D as Plot2D
from MPSPlots.Math import Sp2Cart, RotateX


class Stokes():
    # https://en.wikipedia.org/wiki/Stokes_parameters
    r"""Dict subclass representing scattering Far-field in the Stokes
    representation.
    | The stokes parameters are:
    |     I : Intensity of the fields
    |     Q : linear polarization parallel to incident polarization
    |     U : linear polarization 45 degree to incident polarization
    |     V : Circular polarization

    .. math:
        I &= \\big| E_x \big|^2 + \\big| E_y \\big|^2

        Q &= \\big| E_x \big|^2 - \\big| E_y \\big|^2

        U &= 2 \\mathcal{Re} \\big\{ E_x E_y^* \\big\}

        V &= 2 \\mathcal{Im} \\big\{ E_x E_y^* \\big\}

    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the Stokes parameters in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the Stokes parameters.

    """

    def __init__(self, Parent, Num: int = 100, Distance: float = 1.):
        self.Parent = Parent

        self.EPhi, self.ETheta, self.Theta, self.Phi = Parent.Bind.FullFields(Sampling=Num, R=1)

        Intensity = numpy.abs(self.EPhi)**2 + numpy.abs(self.ETheta)**2

        self.I = Intensity / numpy.max(Intensity)
        self.Q = (numpy.abs(self.EPhi)**2 - numpy.abs(self.ETheta)**2) / Intensity
        self.U = (+2 * numpy.real(self.EPhi * self.ETheta.conjugate())) / Intensity
        self.V = (-2 * numpy.imag(self.EPhi * self.ETheta.conjugate())) / Intensity
        self.Shape = self.V.shape

    def Plot(self, Source=True, Axes=True, Show=True):

        Phi, Theta = numpy.meshgrid(self.Phi, self.Theta)

        Coordinate = Sp2Cart(R=Phi * 0 + 0.5, Phi=Phi, Theta=Theta)

        figure = Scene3D(shape=(1, 4), window_size=[2500, 800])

        for Plot, Field, Name in zip([(0, 0), (0, 1), (0, 2), (0, 3)],
                                     [self.I, self.Q, self.U, self.V],
                                     ['I', 'Q', 'U', 'V']):
            figure.Add_Mesh(Plot=Plot,
                            Coordinate=Coordinate,
                            scalars=Field.T,
                            cmap='seismic',
                            scalar_bar_args={'title': f'{Name} Amplitude'}
                            )

            figure.__add_axes__(Plot=Plot)
            figure.__add__text__(Plot=Plot, Text=f'{Name} field')

        return figure


class SPF():
    r"""Dict subclass representing scattering phase function of SPF in short.
    The SPF is defined as:
    .. math::
        \\text{SPF} = E_{\\parallel}(\\phi,\\theta)^2 + E_{\\perp}(\\phi,\\theta)^2

    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the SPF in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the SPF.

    """

    def __init__(self, Parent, Num: int = 100, Distance: float = 1.):

        self.Parent = Parent

        self.EPhi, self.ETheta, self.Theta, self.Phi = Parent.Bind.FullFields(Sampling=Num, R=1)

        self.SPF = numpy.sqrt(numpy.abs(self.EPhi)**2 + numpy.abs(self.ETheta)**2)

        self.Shape = self.SPF.shape

    def Plot(self, Source=True, Axes=True, Show=True):

        Scalar = self.SPF / self.SPF.max() * 2

        Phi, Theta = numpy.meshgrid(self.Phi, self.Theta)

        Coordinate = Sp2Cart(R=Scalar, Phi=Phi, Theta=Theta)

        figure = Scene3D(shape=(1, 1), window_size=[1800, 1000])

        Plot = (0, 0)
        figure.Add_Mesh(Plot=Plot,
                        Coordinate=Coordinate,
                        scalars=Scalar.T,
                        scalar_bar_args={'title': 'Intensity'}
                        )

        figure.__add_axes__(Plot=Plot)
        figure.__add__text__(Plot=Plot, Text='Scattering phase function')

        return figure


class S1S2():
    r"""Dict subclass representing S1 and S2 function.
    S1 and S2 are defined as:

    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the S1 and S2 in spherical coord.

    """
    def __init__(self, Parent, Phi: numpy.ndarray = None, Num: int = None):
        self.Parent = Parent

        if Num is None:
            Num = 200

        if Phi is None:
            Phi = numpy.linspace(-180, 180, Num)

        self.S1, self.S2 = Parent.Bind.S1S2(Phi=numpy.deg2rad(Phi)+numpy.pi/2)
        self.Phi = Phi
        self.Shape = Phi.shape

    def Plot(self):

        Figure = Plot2D.Scene2D(UnitSize=(3, 3))

        S1_Ax = Plot2D.Axis(Row=0, Col=0, Projection='polar', Title='S1 parameter')
        S2_Ax = Plot2D.Axis(Row=0, Col=1, Projection='polar', Title='S2 parameter')

        zero = 0 * numpy.abs(self.S1)
        S1_artist = Plot2D.FillLine(X=numpy.deg2rad(self.Phi), Y0=zero, Y1=numpy.abs(self.S1), Color='C0', LineStyle='-')
        S2_artist = Plot2D.FillLine(X=numpy.deg2rad(self.Phi), Y0=zero, Y1=numpy.abs(self.S2), Color='C1', LineStyle='-')

        S1_Ax.AddArtist(S1_artist)
        S2_Ax.AddArtist(S2_artist)

        Figure.AddAxes(S1_Ax, S2_Ax)

        return Figure


class FarField():
    r"""Dict subclass representing scattering Far-field in a spherical
    coordinate representation.
    The Far-fields are defined as:

    .. math::
        \\text{Fields} = E_{||}(\\phi,\\theta)^2, E_{\\perp}(\\phi,\\theta)^2

    Parameters
    ----------
    Parent : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the far-fields in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the far-fields.
    """

    def __init__(self, Num: int = 200, Parent=None, Distance: float = 1.):
        self.Parent = Parent

        self.EPhi, self.ETheta, self.Theta, self.Phi = Parent.Bind.FullFields(Sampling=Num, R=1)

        self.Shape = self.EPhi.shape

    def Plot(self, Source=True, Axes=True, Show=True):
        Phi, Theta = numpy.meshgrid(self.Phi, self.Theta)

        Coordinate = Sp2Cart(R=Phi * 0 + 0.5, Phi=Phi, Theta=Theta)

        figure = Scene3D(shape=(1, 4), window_size=[2500, 800])

        for Plot, Field, Name in zip([(0, 0), (0, 1), (0, 2), (0, 3)],
                                     [self.EPhi.real, self.EPhi.imag, self.ETheta.real, self.ETheta.imag],
                                     ['Phi real', 'Phi imaginary', 'Theta real', 'Theta imaginary']):
            figure.Add_Mesh(Plot=Plot,
                            Coordinate=Coordinate,
                            scalars=Field.T,
                            cmap='seismic',
                            scalar_bar_args={'title': f'{Name} Amplitude'}
                            )

            if 'Phi' in Name:
                figure.Add_phi_vector_field(Plot)
            elif 'Theta' in Name:
                figure.Add_theta_vector_field(Plot)

            figure.__add_axes__(Plot=Plot)
            figure.__add__text__(Plot=Plot, Text=f'{Name} field')

        return figure


class Footprint():
    r"""Dict subclass representing footprint of the scatterer.
    The footprint usually depend on the scatterer and the detector.
    For more information see references in the
    `documentation <https://pymiesim.readthedocs.io/en/latest>`_
    The footprint is defined as:

    .. math::
        \\text{Footprint} = \\big| \\mathscr{F}^{-1} \\big\\{ \\tilde{ \\psi }\
        (\\xi, \\nu), \\tilde{ \\phi}_{l,m}(\\xi, \\nu)  \\big\\} \
        (\\delta_x, \\delta_y) \\big|^2


    Parameters
    ----------
    Scatterer : :class:`Scatterer`
        The scatterer.
    Detector : :class:`Detector`
        The detector.
    Num : :class:`int`
        Number of point to evaluate the footprint in cartesian coord.

    """

    def __init__(self, Scatterer, Detector):
        self.Detector = Detector
        self.Scatterer = Scatterer
        self.PaddingFactor = 10

        self.Sampling = 500 if isinstance(Detector, PyMieSim.Detector.LPmode) else Detector.Sampling

        self.ComputeFootprint()

    def ComputeFootprint(self):

        Phi, Theta = numpy.mgrid[-self.Detector.MaxAngle:self.Detector.MaxAngle:complex(self.Sampling),
                                 0:numpy.pi:complex(self.Sampling)]

        MaxDirect = 1 / (numpy.sin(self.Detector.MaxAngle) * self.Scatterer.Source.k / (2 * numpy.pi))

        X = Y = numpy.linspace(-1, 1, self.Sampling) * self.Sampling / 2 * MaxDirect / self.PaddingFactor

        _, Phi, Theta = RotateX(Phi + numpy.pi / 2, Theta, numpy.pi / 2)

        FarFieldPara, FarFieldPerp = self.Scatterer._FarField(Phi.flatten() + numpy.pi / 2,
                                                              Theta.flatten(),
                                                              1.0,
                                                              Structured=False)

        ScalarField = self.Detector.GetStructuredScalarField()[0]

        Perp = ScalarField * FarFieldPerp.reshape(Theta.shape)

        Para = ScalarField * FarFieldPara.reshape(Theta.shape)

        FourierPara = self.GetFourierComponent(Para)
        FourierPerp = self.GetFourierComponent(Perp)

        self.Map = (FourierPara + FourierPerp)
        self.DirectX = X
        self.DirectY = Y

    def GetFourierComponent(self, Scalar):
        TotalSize = self.Sampling * self.PaddingFactor

        start = int(TotalSize / 2 - numpy.floor(self.Sampling / 2))
        end = int(TotalSize / 2 + numpy.ceil(self.Sampling / 2))

        Fourier = numpy.fft.ifft2(Scalar, s=[TotalSize, TotalSize])

        Fourier = numpy.abs(numpy.fft.fftshift(Fourier))**2

        return Fourier[start: end, start: end]

    def Plot(self):

        Figure = Plot2D.Scene2D(UnitSize=(6, 6))

        Ax = Plot2D.Axis(Row=0, Col=0,
                         Title='Scatterer Footprint',
                         xLabel=r'Offset distance in X-axis [$\mu$m]',
                         yLabel=r'Offset distance in Y-axis [$\mu$m]',)

        artist = Plot2D.Mesh(X=self.DirectY * 1e6,
                             Y=self.DirectX * 1e6,
                             Scalar=self.Map,
                             ColorMap='gray')

        Ax.AddArtist(artist)

        Figure.AddAxes(Ax)

        return Figure


# -
