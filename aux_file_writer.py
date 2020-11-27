from Constants.constants import *
import numpy as np

for temp in TEMPS:
    print(temp)
    file = '{}OUTPUT/photz_{}k.zout'.format(ROOT, temp)
    zout = np.loadtxt(file, skiprows=2)
    z = zout[:, [5]]
    np.save('{}Auxiliary_Files/{}.npy'.format(ROOT, temp), z)

file = '{}OUTPUT/photz_31k.zout'.format(ROOT)
ids = np.loadtxt(file, skiprows=2, usecols=0)
np.save('{}Auxiliary_Files/ids.npy'.format(ROOT), ids)
