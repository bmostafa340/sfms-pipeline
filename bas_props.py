from Constants.constants import *
import numpy as np

D_BAS = 560
N_PROPS = 5

SCL = 3.e18 / 12357.0

METS = [0.0001, 0.0010, 0.0020, 0.0030, 0.0040, 0.0060, 0.0080, 0.0100,
        0.0140, 0.0200, 0.0300, 0.0400]

file = '{}Extra/nmf_QSF_v3_12_00028.npy'.format(ROOT)
nmf = np.load(file, allow_pickle=True)

temp_norm = nmf[0] * SCL
coeffs = (nmf[1].T / nmf[1].sum(axis=1)).T

file = '{}Extra/NMF_Props/{}'.format(ROOT, 20)
with open(file, 'r') as f:
    header_props = f.readline().split()[1:]

mass_idx, sfr_idx, age_idx, Av_idx, met_idx, Lv_idx = \
    header_props.index('mass'), header_props.index('sfr'), \
    header_props.index('age'), header_props.index('Av'), \
    header_props.index('zmet'), header_props.index('Lv')

for temp in TEMPS:
    file = '{}Extra/NMF_Props/{}'.format(ROOT, temp)
    fsps_props = np.loadtxt(file, skiprows=1)

    # computing properties for normalized fsps basis templates
    mass_temp = fsps_props[:, mass_idx] / temp_norm
    sfr_temp = fsps_props[:, sfr_idx] / temp_norm
    Lv_temp = fsps_props[:, Lv_idx] / temp_norm
    age_temp = fsps_props[:, age_idx]
    met_temp = np.array([METS[int(i)] for i in fsps_props[:, met_idx]])
    dust_temp = 2.512 ** fsps_props[:, Av_idx]

    # standard linear combinations where appropriate
    mass = np.matmul(coeffs, mass_temp)
    sfr = np.matmul(coeffs, sfr_temp)
    Lv = np.matmul(coeffs, Lv_temp)

    # mass-weighting where appropriate

    # weighted_coeffs - multiplying coefficients by the masses of
    #                   their corresponding template
    # dimensions - 12 x 560
    # [[c_1_1 * m1 , c_1_2 * m2 , ... , c_1_560 * m560 ]
    #  [c_2_1 * m1 , c_2_2 * m2 , ... , c_2_560 * m560 ]
    #  ...
    #  [c_12_1 * m1, c_12_2 * m2, ... , c_12_560 * m560]]
    weighted_coeffs = coeffs * mass_temp

    # denom - factor used to normalize by Σ(m_i * c_i)
    # dimensions - 1 x 12
    # [b1: Σ(m_i * c_i), b2: Σ(m_i * c_i), ... , b12: Σ(m_i * c_i)]
    denom = np.matmul(coeffs, mass_temp)

    age = np.matmul(weighted_coeffs, age_temp) / denom
    met = np.matmul(weighted_coeffs, met_temp) / denom

    # base change formula to calculate log_2.512 of each element
    Av = np.log(np.matmul(weighted_coeffs, dust_temp) / denom) / np.log(2.512)

    props = np.array([mass, sfr, age, Av, met, Lv]).T

    file = '{}Computed_Files/Basis_Props/{}.npy'.format(ROOT, temp)
    np.save(file, props)
