"""
==========================
S1 S2 function computation
==========================

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    Source = PlaneWave(wavelength=450e-9,
                       polarization=0,
                       amplitude=1)

    Scat = Sphere(diameter=600e-9,
                  source=Source,
                  index=1.4)

    S1S2 = Scat.get_s1s2(Num=200)

    S1S2.Plot().Show()


if __name__ == '__main__':
    run()
