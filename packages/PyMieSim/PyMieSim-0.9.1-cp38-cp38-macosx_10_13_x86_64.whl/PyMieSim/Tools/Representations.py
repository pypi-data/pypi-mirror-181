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
    |     I : intensity of the fields
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
    parent_scatterer : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the Stokes parameters in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the Stokes parameters.

    """

    def __init__(self, parent_scatterer, Num: int = 100, Distance: float = 1.):
        self.parent_scatterer = parent_scatterer

        self.E_phi, self.E_theta, self.theta, self.phi = parent_scatterer.Bind.FullFields(sampling=Num, r=1)

        intensity = numpy.abs(self.E_phi)**2 + numpy.abs(self.E_theta)**2

        self.I = intensity / numpy.max(intensity)
        self.Q = (numpy.abs(self.E_phi)**2 - numpy.abs(self.E_theta)**2) / intensity
        self.U = (+2 * numpy.real(self.E_phi * self.E_theta.conjugate())) / intensity
        self.V = (-2 * numpy.imag(self.E_phi * self.E_theta.conjugate())) / intensity
        self.Shape = self.V.shape

    def Plot(self, show_ource=True, show_axes=True):

        phi, theta = numpy.meshgrid(self.phi, self.theta)

        Coordinate = Sp2Cart(R=phi * 0 + 0.5, Phi=phi, Theta=theta)

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
    parent_scatterer : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the SPF in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the SPF.

    """

    def __init__(self, parent_scatterer, Num: int = 100, Distance: float = 1.):

        self.parent_scatterer = parent_scatterer

        self.E_phi, self.E_theta, self.theta, self.phi = parent_scatterer.Bind.FullFields(sampling=Num, r=1)

        self.SPF = numpy.sqrt(numpy.abs(self.E_phi)**2 + numpy.abs(self.E_theta)**2)

        self.Shape = self.SPF.shape

    def Plot(self, show_source=True, show_axes=True):

        Scalar = self.SPF / self.SPF.max() * 2

        Phi, Theta = numpy.meshgrid(self.phi, self.theta)

        Coordinate = Sp2Cart(R=Scalar, Phi=Phi, Theta=Theta)

        figure = Scene3D(shape=(1, 1), window_size=[1800, 1000])

        Plot = (0, 0)
        figure.Add_Mesh(Plot=Plot,
                        Coordinate=Coordinate,
                        scalars=Scalar.T,
                        scalar_bar_args={'title': 'intensity'}
                        )

        figure.__add_axes__(Plot=Plot)
        figure.__add__text__(Plot=Plot, Text='Scattering phase function')

        return figure


class S1S2():
    r"""Dict subclass representing S1 and S2 function.
    S1 and S2 are defined as:

    Parameters
    ----------
    parent_scatterer : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the S1 and S2 in spherical coord.

    """
    def __init__(self, parent_scatterer, Phi: numpy.ndarray = None, Num: int = None):
        self.parent_scatterer = parent_scatterer

        if Num is None:
            Num = 200

        if Phi is None:
            Phi = numpy.linspace(-180, 180, Num)

        self.S1, self.S2 = parent_scatterer.Bind.S1S2(phi=numpy.deg2rad(Phi) + numpy.pi / 2)
        self.phi = Phi
        self.Shape = Phi.shape

    def Plot(self):

        Figure = Plot2D.Scene2D(unit_size=(3, 3))

        S1_Ax = Plot2D.Axis(row=0, col=0, projection='polar', title='S1 parameter')
        S2_Ax = Plot2D.Axis(row=0, col=1, projection='polar', title='S2 parameter')

        zero = 0 * numpy.abs(self.S1)
        S1_artist = Plot2D.FillLine(x=numpy.deg2rad(self.phi), y0=zero, y1=numpy.abs(self.S1), color='C0', line_style='-')
        S2_artist = Plot2D.FillLine(x=numpy.deg2rad(self.phi), y0=zero, y1=numpy.abs(self.S2), color='C1', line_style='-')

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
    parent_scatterer : :class:`Scatterer`
        The scatterer parent.
    Num : :class:`int`
        Number of point to evaluate the far-fields in spherical coord.
    Distance : :class:`float`
        Distance at which we evaluate the far-fields.
    """

    def __init__(self, Num: int = 200, parent_scatterer=None, Distance: float = 1.):
        self.parent_scatterer = parent_scatterer

        self.E_phi, self.E_theta, self.theta, self.phi = parent_scatterer.Bind.FullFields(sampling=Num, r=1)

        self.Shape = self.E_phi.shape

    def Plot(self, show_ource=True, show_axes=True):
        Phi, Theta = numpy.meshgrid(self.phi, self.theta)

        Coordinate = Sp2Cart(R=Phi * 0 + 0.5, Phi=Phi, Theta=Theta)

        figure = Scene3D(shape=(1, 4), window_size=[2500, 800])

        for Plot, Field, Name in zip([(0, 0), (0, 1), (0, 2), (0, 3)],
                                     [self.E_phi.real, self.E_phi.imag, self.E_theta.real, self.E_theta.imag],
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
    scatterer : :class:`Scatterer`
        The scatterer.
    detector : :class:`Detector`
        The detector.
    Num : :class:`int`
        Number of point to evaluate the footprint in cartesian coord.

    """

    def __init__(self, scatterer, detector):
        self.detector = detector
        self.scatterer = scatterer
        self.padding_factor = 10

        self.sampling = 500 if isinstance(detector, PyMieSim.Detector.LPmode) else detector.sampling

        self._compute_footprint_()

    def _compute_footprint_(self):

        phi, theta = numpy.mgrid[-self.detector.max_angle:self.detector.max_angle:complex(self.sampling),
                                 0:numpy.pi:complex(self.sampling)]

        max_direct = 1 / (numpy.sin(self.detector.max_angle) * self.scatterer.source.k / (2 * numpy.pi))

        x = y = numpy.linspace(-1, 1, self.sampling) * self.sampling / 2 * max_direct / self.padding_factor

        _, phi, theta = RotateX(phi + numpy.pi / 2, theta, numpy.pi / 2)

        far_field_para, far_field_perp = self.scatterer._FarField(phi=phi.flatten() + numpy.pi / 2,
                                                                  theta=theta.flatten(),
                                                                  r=1.0,
                                                                  structured=False)

        scalarfield = self.detector.get_structured_scalarfield()[0]

        perp = scalarfield * far_field_perp.reshape(theta.shape)

        para = scalarfield * far_field_para.reshape(theta.shape)

        fourier_para = self.GetFourierComponent(para)
        fourier_perp = self.GetFourierComponent(perp)

        self.mapping = (fourier_para + fourier_perp)
        self.direct_x = x
        self.direct_y = y

    def GetFourierComponent(self, scalar):
        total_size = self.sampling * self.padding_factor

        start = int(total_size / 2 - numpy.floor(self.sampling / 2))
        end = int(total_size / 2 + numpy.ceil(self.sampling / 2))

        fourier = numpy.fft.ifft2(scalar, s=[total_size, total_size])

        fourier = numpy.abs(numpy.fft.fftshift(fourier))**2

        return fourier[start: end, start: end]

    def Plot(self):

        Figure = Plot2D.Scene2D(unit_size=(6, 6))

        Ax = Plot2D.Axis(row=0, col=0,
                         title='Scatterer Footprint',
                         x_label=r'Offset distance in X-axis [$\mu$m]',
                         y_label=r'Offset distance in Y-axis [$\mu$m]',)

        artist = Plot2D.Mesh(x=self.direct_y * 1e6,
                             y=self.direct_x * 1e6,
                             scalar=self.mapping,
                             colormap='gray')

        Ax.AddArtist(artist)

        Figure.AddAxes(Ax)

        return Figure


# -
