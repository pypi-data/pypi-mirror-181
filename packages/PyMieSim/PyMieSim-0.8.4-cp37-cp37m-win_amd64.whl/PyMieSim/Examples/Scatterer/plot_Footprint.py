"""
===================
Scatterer footprint
===================

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Detector import LPmode
    from PyMieSim.Source import PlaneWave
    from PyOptik import ExpData

    Detector = LPmode(Mode="2-1", NA=0.3, Sampling=200, GammaOffset=0, PhiOffset=0, CouplingMode='Point')

    Source = PlaneWave(Wavelength=450e-9,
                       Polarization=0,
                       Amplitude=1)

    Scat = Sphere(Diameter=2000e-9,
                  Source=Source,
                  Material=ExpData('BK7'))

    Footprint = Detector.Footprint(Scat)

    Footprint.Plot().Show()


if __name__ == '__main__':
    run()
