import numpy as np

ROOT = '/home/basel/Dropbox/basel/Clean_2015/'

TEMPS = np.arange(8, 61, 1)

TEMP_IDXS = {}
for i, temp in enumerate(TEMPS):
    TEMP_IDXS[temp] = i

Nr, Nc = 4, 6

MIN_Z = 0.25
MAX_Z = 6.00

NTEMP = 12

NOBJ = 518405
NGAL = 1561
