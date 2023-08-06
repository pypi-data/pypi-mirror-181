"""

Photodiode detector
===================

"""


def run():
    from PyMieSim.Detector import Photodiode

    Detector = Photodiode(NA=0.8,
                          sampling=500,
                          gamma_offset=0,
                          phi_offset=0,
                          filter=None)

    Detector.Plot().Show()


if __name__ == '__main__':
    run()
