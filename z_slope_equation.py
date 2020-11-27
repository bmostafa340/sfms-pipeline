from Constants.constants import *

file = '{}Computed_Files/slopes_z_fit'.format(ROOT)
slope_info = np.loadtxt(file)

slope = slope_info[0, :]
slope_err = slope_info[1, :]

slope_const = slope[1]
slope_const_err = slope_err[1]
slope_var = slope[0]
slope_var_err = slope_err[0]

print('slope = {} +/- {} + {} +/- {} x t'.format(
    slope_const, slope_const_err, slope_var, slope_var_err))
