"""
Photodiode Coupling
===================
"""
# sphinx_gallery_thumbnail_path = '../images/Extras/Coupling.png'


def run():
    from PyMieSim.Source import PlaneWave
    from PyMieSim.Detector import LPmode
    from PyMieSim.Scatterer import Sphere

    Source = PlaneWave(Wavelength=450e-9,
                       Polarization=0,
                       Amplitude=1)

    Detector = LPmode(Mode=(1, 1),
                      Sampling=600,
                      NA=0.2,
                      GammaOffset=180,
                      PhiOffset=0,
                      CouplingMode='Point')

    Scat = Sphere(Diameter=300e-9,
                  Source=Source,
                  Index=1.4)

    Coupling = Detector.Coupling(Scatterer=Scat)

    print(Coupling)  # 6.566085549292496e-18 Watt  (6.57e-03 fWatt)


if __name__ == '__main__':
    run()
