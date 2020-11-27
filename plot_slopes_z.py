from Constants.constants import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.odr as regression
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u


def line(B, x):
    return B[0] * x + B[1]


START = 0
END = 25

COSMO = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)

slopes = list(np.loadtxt('{}Computed_Files/slopes_z'.format(ROOT)))
err = list(np.loadtxt('{}Computed_Files/slope_errs_z'.format(ROOT)))

univ_age = []
for i in range(Nr * Nc):
    lower_z = i / (Nr * Nc) * (MAX_Z - MIN_Z) + MIN_Z
    upper_z = lower_z + 1 / (Nr * Nc) * (MAX_Z - MIN_Z)
    min_age = COSMO.age(lower_z).value
    max_age = COSMO.age(upper_z).value
    age = (min_age + max_age) / 2
    univ_age.append(age)

slopes = slopes[START:END]
err = err[START:END]
univ_age = univ_age[START:END]

coeff = np.polyfit(univ_age, slopes, 1)
linear = regression.Model(line)
mydata = regression.Data(univ_age, slopes)
myodr = regression.ODR(mydata, linear, beta0=coeff)
output = myodr.run()
coeff = output.beta
error = output.sd_beta

np.savetxt('{}Computed_Files/slopes_z_fit'.format(ROOT), np.array([coeff, error]))

fit_x = [COSMO.age(6).value, COSMO.age(0).value]
fit_y = line(coeff, np.array(fit_x))

plt.errorbar(univ_age, slopes, yerr=err, fmt='o', linestyle='None')
plt.plot(fit_x, fit_y)

plt.xlabel('Age of Universe [Gyr]')
plt.ylabel('z-binned SFGMS slopes')

plt.show()
