from Constants.constants import *
import numpy as np
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u

COSMO = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)

idxs = np.load('{}Computed_Files/catalog_idxs.npy'.format(ROOT))

file = '{}OUTPUT/photz{}.coeff'.format(ROOT, 20)
with open(file, 'rb') as f:
    np.fromfile(file=f, dtype=np.int32, count=4)
    c = np.fromfile(file=f, dtype=np.double, count=NTEMP * NOBJ)

# coeffs_temp - galactic coordinates in terms of basis:
# dimensions: NOBJ x 12
# [[c1_g1  , c2_g1   , ... , c12_g1   ]
#  [c1_g2  , c2_g2   , ... , c12_g2   ]
#  ...
#  [c1_NOBJ, c2_gNOBJ, ... , c12_gNOBJ]]
basis_coeffs = c.reshape(NOBJ, NTEMP)[idxs, :]

header_props = ['mass', 'sfr', 'age', 'Av', 'met', 'Lv']
Lv_idx = header_props.index('Lv')
mass_idx = header_props.index('mass')
sfr_idx = header_props.index('sfr')
age_idx = header_props.index('age')
Av_idx = header_props.index('Av')
met_idx = header_props.index('met')

# basis_props - properties of template "galaxies"
# dimensions - 12 x 6
# st_mass, sfr, age, Av, met, Lv
# [[a1 , b1 , ... , f1 ]
#  [a2 , b2 , ... , f2 ]
#  ...
#  [a12, b12, ... , f12]]
file = '{}Computed_Files/Basis_Props/{}.npy'.format(ROOT, 20)
basis_props = np.load(file)

file = '{}Extra/idtempz.txt'.format(ROOT)
idtempz = np.loadtxt(file)
z = idtempz[:, 2]
ids = idtempz[:, [0]]
temp = np.array([20 for i in range(len(ids))]).reshape((-1, 1))

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

glxy_props = np.append(temp, props, 1)
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

np.save('{}Computed_Files/sf_idtemp_idxs_pure_uvj_20K.npy'.format(ROOT), star_forming_idxs)
np.save('{}Computed_Files/quiescent_idtemp_idxs_pure_uvj_20K.npy'.format(ROOT), quiescent_idxs)

is_star_forming = np.zeros((NGAL, 1))
is_quiescent = np.zeros((NGAL, 1))

for i in star_forming_idxs:
    is_star_forming[i][0] = 1

for i in quiescent_idxs:
    is_quiescent[i][0] = 1

glxy_props = np.append(glxy_props, is_star_forming, 1)
glxy_props = np.append(glxy_props, is_quiescent, 1)

file = '{}Computed_Files/galaxy_properties_pure_uvj_20K.npy'.format(ROOT)
np.save(file, glxy_props)

file = '{}Computed_Files/galaxy_properties_pure_uvj_20K'.format(ROOT)
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
