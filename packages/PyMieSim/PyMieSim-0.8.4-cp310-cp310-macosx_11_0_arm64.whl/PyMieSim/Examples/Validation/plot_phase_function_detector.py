"""
===============================
Goniometrique coupling vs S1 S2
===============================

"""


def run():
    import numpy
    import matplotlib.pyplot as plt
    from PyMieSim.Experiment import SphereSet, SourceSet, Setup, PhotodiodeSet
    from PyMieSim import Measure
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    scatterer_diameter = 0.3e-6
    scatterer_index = 1.4
    source_wavelength = 1.2e-6 

    scatSet = SphereSet(Diameter=scatterer_diameter,
                        Index=scatterer_index,
                        nMedium=1.0)

    sourceSet = SourceSet(Wavelength=source_wavelength,
                          Polarization=[0, 90],
                          Amplitude=1)

    detecSet = PhotodiodeSet(NA=[0.1],
                             PhiOffset=numpy.linspace(-180, 180, 100),
                             GammaOffset=0.0,
                             Sampling=1000,
                             Filter=None)

    Experiment = Setup(scatSet, sourceSet, detecSet)

    Data = Experiment.Get([Measure.Coupling])

    source = PlaneWave(Wavelength=source_wavelength, Polarization=90, Amplitude=1)
    scatterer = Sphere(Diameter=scatterer_diameter, Source=source, Index=scatterer_index, nMedium=1.0)
    data = scatterer.S1S2()
    phi, s1, s2 = data.Phi, data.S1, data.S2

    figure, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 4), subplot_kw={'projection': 'polar'})

    Data0_S1 = numpy.abs(s1)**2
    Data0_S1 /= Data0_S1.max()
    Data0_S2 = numpy.abs(s2)**2
    Data0_S2 /= Data0_S2.max()

    Data1 = Data.Data.squeeze()
    Data1 /= Data1.max()

    ax0.plot(numpy.deg2rad(phi), Data0_S1, linewidth=3, zorder=1, label='Computed s1')
    ax0.plot(numpy.deg2rad(detecSet.PhiOffset.Values.squeeze()), Data1[0], linestyle='--', color='k', zorder=10, label='Computed coupling for polarization: 0')

    ax1.plot(numpy.deg2rad(phi), Data0_S2, linewidth=3, zorder=1, label='Computed s2')
    ax1.plot(numpy.deg2rad(detecSet.PhiOffset.Values.squeeze()), Data1[1], linestyle='--', color='k', zorder=10, label='Computed coupling for polarization: 90')

    ax0.legend()
    ax1.legend()
    plt.show()


if __name__ == '__main__':
    run()
