#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def FraunhoferDiffraction(nearField):
    r"""Function compute the Far-Field of a given Near-Field using Fraunhofer
    relation under approximation of small angle.

    Parameters
    ----------
    nearField : :class:`np.ndarray`
        Near-Field input [2D].

    Returns
    -------
    :class:`np.ndarray`
        Far-Field ouptut [2D].

    """
    temp = np.fft.fft2(nearField)

    temp /= GenShift(temp.shape[0])

    return np.fft.fftshift(temp)


def GenShift(npts):
    r"""Function generate a complex shift array that has to be multiplied to FFT in order to obtain
    a phase accurate Fourier transform.

    Parameters
    ----------
    npts : :class:`int`
        Number of point (per dimension) of the FFT array.

    Returns
    -------
    :class:`np.ndarray`
        Complex array for FFT.

    """
    if npts % 2 == 1:
        phase_shift = np.exp(-complex(0, 1) * np.pi * np.arange(npts) * (npts - 1) / npts)

        shift_grid, _ = np.meshgrid(phase_shift, phase_shift)

        return shift_grid * shift_grid.T

    else:
        phase_shift = np.exp(-complex(0, 1) * np.pi * np.arange(npts) * (npts) / npts)

        shift_grid, _ = np.meshgrid(phase_shift, phase_shift)

        return shift_grid * shift_grid.T
