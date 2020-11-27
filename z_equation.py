# Run slope_z_univ_age and intercept_z_univ_age

import math
from Constants.constants import *
from astropy.cosmology import FlatLambdaCDM, z_at_value
import astropy.units as u

COSMO = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)

file = '{}Computed_Files/slopes_z_fit'.format(ROOT)
slope_info = np.loadtxt(file)

file = '{}Computed_Files/intercepts_9_z_fit'.format(ROOT)
intercept_info = np.loadtxt(file)

slope = slope_info[0, :]
slope_err = slope_info[1, :]

intercept = intercept_info[0, :]
intercept_err = intercept_info[1, :]

slope_const = slope[1]
slope_const_err = slope_err[1]
slope_var = slope[0]
slope_var_err = slope_err[0]

intercept_const = intercept[1]
intercept_const_err = intercept_err[1]
intercept_var = intercept[0]
intercept_var_err = intercept_err[0]

print('log SFR - ({:<6} +/- {:<6} + {:<6} +/- {:<6} x t) = '
      '({:<6} +/- {:<6} + {:<6} +/- {:<6} x t) (log M - 9)'.format(
    str(intercept_const)[:6], str(intercept_const_err)[:6],
    str(intercept_var)[:6], str(intercept_var_err)[:6],
    str(slope_const)[:6], str(slope_const_err)[:6],
    str(slope_var)[:6], str(slope_var_err)[:6]))

intercept_const = intercept[1] - 9 * slope_const
intercept_const_err = \
    math.sqrt(intercept_err[1] ** 2 + (9 * slope_const_err) ** 2)
intercept_var = intercept[0] - 9 * slope_var
intercept_var_err = \
    math.sqrt(intercept_err[0] ** 2 + (9 * slope_var_err) ** 2)

print('log SFR = ({:<6} +/- {:<6} + {:<6} +/- {:<6} x t) log M + '
      '({:<6} +/- {:<6} + {:<6} +/- {:<6} x t)'.format(
    str(slope_const)[:6], str(slope_const_err)[:6],
    str(slope_var)[:6], str(slope_var_err)[:6],
    str(intercept_const)[:6], str(intercept_const_err)[:6],
    str(intercept_var)[:6], str(intercept_var_err)[:6]))

intercepts = list(np.loadtxt('{}Computed_Files/intercepts_9_z'.format(ROOT)))
slopes = list(np.loadtxt('{}Computed_Files/slopes_z'.format(ROOT)))
intercepts_20K = list(np.loadtxt('{}Computed_Files/intercepts_9_z_20K'.format(ROOT)))
slopes_20K = list(np.loadtxt('{}Computed_Files/slopes_z_20K'.format(ROOT)))

for i in range(Nr * Nc):
    lower_z = i / (Nr * Nc) * (MAX_Z - MIN_Z) + MIN_Z
    upper_z = lower_z + 1 / (Nr * Nc) * (MAX_Z - MIN_Z)
    min_age = COSMO.age(lower_z).value
    max_age = COSMO.age(upper_z).value
    age = (min_age + max_age) / 2
    z = z_at_value(COSMO.age, age * u.Gyr)
    print('         {} & {} & {} & {} & {} & {} \\\\'.format(
        str(z)[:4], str(age)[:4], str(slopes[i])[:4],
        str(slopes_20K[i])[:4], str(intercepts[i])[:4], str(intercepts_20K[i])[:4]))
