"""
===============
SPF computation
===============

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    Source = PlaneWave(Wavelength=500e-9,
                       Polarization=0,
                       Amplitude=1)

    Scat = Sphere(Diameter=1200e-9,
                  Source=Source,
                  Index=1.4,
                  nMedium=1.0)

    SPF = Scat.SPF(Num=300)

    SPF.Plot().Show()


if __name__ == '__main__':
    run()
