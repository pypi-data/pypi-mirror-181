"""

Photodiode detector
===================

"""


def run():
    from PyMieSim.Detector import Photodiode

    Detector = Photodiode(NA=0.8,
                          Sampling=500,
                          GammaOffset=0,
                          PhiOffset=0,
                          Filter=None)

    Detector.Plot().Show()


if __name__ == '__main__':
    run()
