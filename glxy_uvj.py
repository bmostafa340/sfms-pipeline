from Constants.constants import *

uvj_fluxes = []

for temp in TEMPS:
    file = '{}Computed_Files/UVJ_By_Temp/{}.npy'.format(ROOT, temp)
    uvj_temp = np.load(file)
    for arr in uvj_temp:
        uvj_fluxes.append([int(arr[0]), arr[1], arr[2]])

uvj_fluxes.sort()

file = '{}Computed_Files/galaxy_uvj.npy'.format(ROOT)
np.save(file, uvj_fluxes)

file = '{}Computed_Files/galaxy_uvj'.format(ROOT)
with open(file, 'w') as f:
    for line in uvj_fluxes:
        f.write('{} {} {}\n'.format(
            int(line[0]),
            str(float(line[1])),
            str(float(line[2]))
        ))
