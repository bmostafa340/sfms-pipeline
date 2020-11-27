from Constants.constants import *

file = '{}Computed_Files/intercepts_9_z_fit'.format(ROOT)
intercept_info = np.loadtxt(file)

intercept = intercept_info[0, :]
intercept_err = intercept_info[1, :]

intercept_const = intercept[1]
intercept_const_err = intercept_err[1]
intercept_var = intercept[0]
intercept_var_err = intercept_err[0]

print('intercept = {} +/- {} + {} +/- {} x t'.format(
    intercept_const, intercept_const_err,
    intercept_var, intercept_var_err
))
