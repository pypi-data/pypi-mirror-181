"""
======================
Far-Fields computation
======================

"""


def run():
    from PyMieSim.Scatterer import Sphere
    from PyMieSim.Source import PlaneWave

    Source = PlaneWave(Wavelength=1000e-9,
                       Polarization=0,
                       Amplitude=1)

    Scat = Sphere(Diameter=1500e-9,
                  Source=Source,
                  Index=1.4)

    Fields = Scat.FarField(Num=300)

    Fields.Plot().Show()


if __name__ == '__main__':
    run()
