# Adapted from code produced by Hagan Hensley

from Constants.constants import *
import numpy as np
import peakutils

zout = []
MIN_TEMP = 8
CUTOFF_TEMP = 60
STEP_SIZE = 1
tempsrange = range(MIN_TEMP, CUTOFF_TEMP + STEP_SIZE, STEP_SIZE)
ROOT_local = '{}OUTPUT/'.format(ROOT)
for temp in tempsrange:
    zout.append(np.loadtxt(ROOT_local + 'photz_{0}k.zout'.format(temp), skiprows = 2))
zout = np.array(zout)

temps = []
z = []
zspec = []
ids = []

zbad = []
CHI_CUTOFF = np.inf
n = 0
for i in range(len(zout[0])):
    print(i / len(zout[0])) #progress meter
    chis = zout[:,i,6]
    local_minima = peakutils.indexes(-chis)
    if not len(local_minima) == 0:
        #finding the best non-edge local chi^2 minimum
        chi_min_index = local_minima[np.argmin(chis[np.isin(np.arange(len(chis)), local_minima)])]
        z_min = zout[chi_min_index][i][5]
        #chi_min = zout[chi_min_index][i][6]
        if z_min > 0: # and z_min < Z_MAX and zspec_obj < Z_MAX:
            temps.append(tempsrange[chi_min_index])
            z.append(z_min)
            ids.append(zout[chi_min_index][i][0])
    else:
        n += 1
        zbad.append(zout[0][i][5])

np.savetxt('{}Extra/idtempz.txt'.format(ROOT), np.c_[np.array(ids), np.array(temps), np.array(z)], fmt = '%f')
