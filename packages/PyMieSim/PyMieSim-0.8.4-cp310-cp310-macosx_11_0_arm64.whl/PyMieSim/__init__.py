from .Tools import Measure
import numpy
import os.path
from PyMieSim.Tools.Directories import LPModePath


def LoadLPMode(ModeNumber, Type: str = 'Unstructured', Sampling: int = 100):

    AllModes = ["0-1", "0-2", "0-3", "1-1", "1-2", "1-3", "2-1", "2-2", "3-1", "3-2", "4-1", "5-1"]
    AllSampling = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    if Type.lower() == 'unstructured':
        filename = f'{ModeNumber}/{Type}{Sampling}.npy'
    elif Type.lower() == 'structured':
        filename = f'{ModeNumber}/{Type}.npy'

    fileDir = os.path.join(LPModePath, filename)

    if not os.path.exists(fileDir):
        raise ValueError(f"""\nFile: {filename} does not exists.
                  \nThis specific LP mode with specific sampling might not be available.
                  \nAvailable modes are {AllModes} \nAvailable sampling are {AllSampling}""")

    return numpy.load(fileDir)
