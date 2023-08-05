"""
==========================
S1 S2 function computation
==========================

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    Source = PlaneWave(Wavelength=450e-9,
                       Polarization=0,
                       Amplitude=1)

    Scat = Sphere(Diameter=600e-9,
                  Source=Source,
                  Index=1.4)

    S1S2 = Scat.S1S2(Num=200)

    S1S2.Plot().Show()


if __name__ == '__main__':
    run()
