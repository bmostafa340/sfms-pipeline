from Constants.constants import *

SF_PERCENTILE = 10
QUIESCENT_PERCENTILE = 90

file = '{}Computed_Files/galaxy_properties_pure_uvj.npy'.format(ROOT)
props = np.load(file)[:, [2, 3]]
sSFR = np.log10(props[:, 1] / props[:, 0])

file = '{}Computed_Files/sf_idtemp_idxs_pure_uvj.npy'.format(ROOT)
sf_idxs = np.load(file)
sf_sSFR = np.take(sSFR, sf_idxs)
print('star-forming {}th percentile log sSFR: {}'.format(
    SF_PERCENTILE, np.percentile(sf_sSFR, SF_PERCENTILE)))

file = '{}Computed_Files/quiescent_idtemp_idxs_pure_uvj.npy'.format(ROOT)
quiescent_idxs = np.load(file)
quiescent_sSFR = np.take(sSFR, quiescent_idxs)
print('quiescent {}th percentile log sSFR: {}'.format(
    QUIESCENT_PERCENTILE,
    np.percentile(quiescent_sSFR, QUIESCENT_PERCENTILE)))

pure_uvj = np.load('{}Computed_Files/galaxy_properties_pure_uvj.npy'.format(ROOT))
sSFR_cut = np.copy(pure_uvj)

sf_sSFR_cut = np.percentile(sf_sSFR, SF_PERCENTILE)
q_sSFR_cut = np.percentile(quiescent_sSFR, QUIESCENT_PERCENTILE)
for i in range(len(sSFR_cut)):
    sSFR = np.log10(pure_uvj[i][3] / pure_uvj[i][2])
    if sSFR < sf_sSFR_cut:
        sSFR_cut[i][9] = 0
    if sSFR > q_sSFR_cut:
        sSFR_cut[i][10] = 0

np.save('{}Computed_Files/galaxy_properties.npy'.format(ROOT), sSFR_cut)

sf_idtemp_idxs = []
quiescent_idtemp_idxs = []

for i in range(len(sSFR_cut)):
    if sSFR_cut[i][9] == 1:
        sf_idtemp_idxs.append(i)
    elif sSFR_cut[i][10] == 1:
        quiescent_idtemp_idxs.append(i)

np.save('{}Computed_Files/sf_idtemp_idxs.npy'.format(ROOT), sf_idtemp_idxs)
np.save('{}Computed_Files/quiescent_idtemp_idxs.npy'.format(ROOT), quiescent_idtemp_idxs)
