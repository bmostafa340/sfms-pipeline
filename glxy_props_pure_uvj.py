# Run aux_file_writer.py first if OUTPUT has changed
# Run bas_props.py first if fsps basis or coefficients have changed

from Constants.constants import *
import numpy as np
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

COSMO = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)

file = '{}Auxiliary_Files/ids.npy'.format(ROOT)
ids = np.load(file)

file = '{}Extra/idtempz.txt'.format(ROOT)
arr = np.loadtxt(file)[:, [0, 1]]

idtemp = np.zeros((NGAL, len(arr[0])), dtype=np.int32)
for r in range(len(arr)):
    for c in range(len(arr[0])):
        idtemp[r][c] = int(arr[r][c])

del arr

cat_idxs = []
idtemp_idxs = []
combined_cat_idxs = []
combined_idtemp_idxs = []
for temp in TEMPS:
    cat_idxs.append([])
    idtemp_idxs.append([])
j = 0
for col in range(NOBJ):
    if j < len(idtemp) and ids[col] == idtemp[j][0]:
        idx = TEMP_IDXS.get(idtemp[j][1])
        if idx is not None:
            cat_idxs[idx].append(col)
            idtemp_idxs[idx].append(j)
            combined_cat_idxs.append(col)
            combined_idtemp_idxs.append(j)
        j += 1

np.save('{}Computed_Files/catalog_idxs'.format(ROOT), combined_cat_idxs)
np.save('{}Computed_Files/idtemp_idxs'.format(ROOT), combined_idtemp_idxs)

coeffs = []
for temp in TEMPS:
    file = '{}OUTPUT/photz{}.coeff'.format(ROOT, temp)
    with open(file, 'rb') as f:
        np.fromfile(file=f, dtype=np.int32, count=4)
        c = np.fromfile(file=f, dtype=np.double, count=NTEMP * NOBJ)

    # coeffs_temp - galactic coordinates in terms of basis:
    # dimensions: NOBJ x 12
    # [[c1_g1  , c2_g1   , ... , c12_g1   ]
    #  [c1_g2  , c2_g2   , ... , c12_g2   ]
    #  ...
    #  [c1_NOBJ, c2_gNOBJ, ... , c12_gNOBJ]]
    coeffs_temp = c.reshape(NOBJ, NTEMP)
    coeffs.append(coeffs_temp[cat_idxs[TEMP_IDXS[temp]], :])

header_props = ['mass', 'sfr', 'age', 'Av', 'met', 'Lv']
Lv_idx = header_props.index('Lv')
mass_idx = header_props.index('mass')
sfr_idx = header_props.index('sfr')
age_idx = header_props.index('age')
Av_idx = header_props.index('Av')
met_idx = header_props.index('met')

full_props = []
for temp in TEMPS:
    print(temp)

    idx = TEMP_IDXS[temp]
    basis_coeffs = coeffs[idx]
    if len(basis_coeffs) == 0:
        full_props.append(np.zeros((0, len(header_props) + 1)))
        continue

    file = '{}Auxiliary_Files/{}.npy'.format(ROOT, temp)
    zout = np.load(file)
    if len(cat_idxs[idx]) == 1:
        z = np.zeros(1)
        z[0] = zout[cat_idxs[idx], :][0]
    else:
        z = zout[cat_idxs[idx], :].squeeze()

    # basis_props - properties of template "galaxies"
    # dimensions - 12 x 6
    # st_mass, sfr, age, Av, met, Lv
    # [[a1 , b1 , ... , f1 ]
    #  [a2 , b2 , ... , f2 ]
    #  ...
    #  [a12, b12, ... , f12]]
    file = '{}Computed_Files/Basis_Props/{}.npy'.format(ROOT, temp)
    basis_props = np.load(file)

    Lv_temp = basis_props[:, Lv_idx]
    mass_temp = basis_props[:, mass_idx]
    sfr_temp = basis_props[:, sfr_idx]
    age_temp = basis_props[:, age_idx]
    dust_temp = 2.512 ** basis_props[:, Av_idx]
    met_temp = basis_props[:, met_idx]

    # Produce normalized coeffs by Lv
    Lv_tot = np.matmul(basis_coeffs, Lv_temp)
    coeff_norm = basis_coeffs * Lv_temp
    coeff_norm = (coeff_norm.T / Lv_tot).T

    # Calculate mass to light ratio
    Lv_norm = np.dot(coeff_norm, Lv_temp)
    mass_norm = np.dot(coeff_norm, mass_temp)
    sfr_norm = np.dot(coeff_norm, sfr_temp)

    MLv = mass_norm / Lv_norm
    SLv = sfr_norm / Lv_norm

    Lvtot_Lsol = Lv_tot / (1.0e29 * 3.328e33)
    lumo_dst = \
        np.array([COSMO.luminosity_distance(red).to(u.cm) / u.cm for red in z]).squeeze()
    nuV = (2.998e18 / (5480 * (1.0 + z))).squeeze()

    Lv = 4 * np.pi * Lvtot_Lsol * nuV * lumo_dst ** 2
    mass = Lv * MLv
    sfr = Lv * SLv

    age_temp *= mass_temp
    met_temp *= mass_temp
    dust_temp *= mass_temp

    denom = np.matmul(coeff_norm, mass_temp)

    age = np.matmul(coeff_norm, age_temp) / denom
    met = np.matmul(coeff_norm, met_temp) / denom
    Av = np.log(np.matmul(coeff_norm, dust_temp) / denom) / np.log(2.512)

    props = np.array([mass, sfr, age, Av, met, Lv, z]).T

    full_props.append(props)

sorter = []
for temp in TEMPS:
    idx = TEMP_IDXS[temp]
    for i in range(len(full_props[idx])):
        sorter.append([cat_idxs[idx][i],
                       full_props[idx][i]])
sorter.sort()

glxy_props = np.zeros((NGAL, len(header_props) + 1))
for i in range(len(sorter)):
    glxy_props[i] = sorter[i][1]

ids = idtemp[:, [0]][combined_idtemp_idxs, :]
temps = idtemp[:, [1]][combined_idtemp_idxs, :]

glxy_props = np.append(temps, glxy_props, 1)
glxy_props = np.append(ids, glxy_props, 1)

uvj = np.load('{}Computed_Files/galaxy_uvj.npy'.format(ROOT))
u_v = uvj[:, 1]
v_j = uvj[:, 2]
del uvj

x_arr = [-10, 0.8, 1.6, 1.6]
y_arr = [1.3, 1.3, 2, 10]

star_forming_idxs = []
quiescent_idxs = []
slope = (y_arr[2] - y_arr[1]) / (x_arr[2] - x_arr[1])
for i in range(NGAL):
    if (u_v[i] < y_arr[0] or v_j[i] > x_arr[2] or
            u_v[i] < slope * (v_j[i] - x_arr[1]) - y_arr[1]):
        star_forming_idxs.append(i)
    elif not (u_v[i] < y_arr[0] or v_j[i] > x_arr[2] or
              u_v[i] < slope * (v_j[i] - x_arr[1]) - y_arr[1]):
        quiescent_idxs.append(i)

np.save('{}Computed_Files/sf_idtemp_idxs_pure_uvj.npy'.format(ROOT), star_forming_idxs)
np.save('{}Computed_Files/quiescent_idtemp_idxs_pure_uvj.npy'.format(ROOT), quiescent_idxs)

is_star_forming = np.zeros((NGAL, 1))
is_quiescent = np.zeros((NGAL, 1))

for i in star_forming_idxs:
    is_star_forming[i][0] = 1

for i in quiescent_idxs:
    is_quiescent[i][0] = 1

glxy_props = np.append(glxy_props, is_star_forming, 1)
glxy_props = np.append(glxy_props, is_quiescent, 1)

file = '{}Computed_Files/galaxy_properties_pure_uvj.npy'.format(ROOT)
np.save(file, glxy_props)

file = '{}Computed_Files/galaxy_properties_pure_uvj'.format(ROOT)
with open(file, 'w') as f:
    f.write('# ID temp st_mass sfr age Av met Lv z is_star_forming is_quiescent\n')
    for col in range(NGAL):
        f.write('{:<8}  {:<2}  {:<18}  {:<18}  {:<18}  '
                '{:<19}  {:<20}  {:<20}  {:<5}  {:<1}  {:<1}\n'.format(
            str(int(glxy_props[col][0]))[:8],
            str(int(glxy_props[col][1]))[:2],
            str(float(glxy_props[col][2]))[:18],
            str(float(glxy_props[col][3]))[:18],
            str(float(glxy_props[col][4]))[:18],
            str(float(glxy_props[col][5]))[:19],
            str(float(glxy_props[col][6]))[:20],
            str(float(glxy_props[col][7]))[:20],
            str(float(glxy_props[col][8]))[:5],
            str(float(glxy_props[col][9]))[:1],
            str(float(glxy_props[col][10]))[:1]
        ))
