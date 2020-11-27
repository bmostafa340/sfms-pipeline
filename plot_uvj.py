from Constants.constants import *
import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors

matplotlib.rc('font', size=9)


def m(val):
    return math.log(val, 10)


Nr, Nc = 6, 5

MIN_X = 0.0
MIN_Y = 0.0
MAX_X = 2.5
MAX_Y = 2.5

MIN_MASS = 7
MAX_MASS = 12

MIN_Z = 0.25
MAX_Z = 6.25

DIVS = []
for i in range(Nr * Nc):
    DIVS.append(50)


x_arr = [-10, 0.8, 1.6, 1.6]
y_arr = [1.3, 1.3, 2, 10]

uvj = np.load('{}Computed_Files/galaxy_uvj.npy'.format(ROOT))
u_v = uvj[:, 1]
v_j = uvj[:, 2]
del uvj

dx, dy = [], []
for i in range(Nr * Nc):
    dy_i = (MAX_Y - MIN_Y) / DIVS[i]
    dx_i = (MAX_X - MIN_X) / DIVS[i]
    dx.append(dx_i)
    dy.append(dy_i)

y, x = [], []
for i in range(Nr * Nc):
    y_i, x_i = np.mgrid[slice(MIN_Y, MAX_Y + dy[i], dy[i]),
                        slice(MIN_X, MAX_X + dx[i], dx[i])]
    x.append(x_i)
    y.append(y_i)

file = '{}Computed_Files/galaxy_properties.npy'.format(ROOT)
c = np.load(file)[:, [2, 3, 8]].T

z = []

for i in range(Nr * Nc):
    lower_z = int(i / Nc) * (MAX_Z - MIN_Z) / Nr + MIN_Z
    upper_z = lower_z + (MAX_Z - MIN_Z) / Nr
    lower_M = (i % Nc) * (MAX_MASS - MIN_MASS) / Nc + MIN_MASS
    upper_M = lower_M + (MAX_MASS - MIN_MASS) / Nc
    data = []
    for r in range(len(y[i]) - 1):
        data.append([])
        for _ in range(len(y[i][0]) - 1):
            data[r].append([])
    for col in range(len(c[0])):
        if np.isnan(u_v[col]) or np.isnan(v_j[col]):
            continue
        if lower_z <= c[2][col] < upper_z and \
                lower_M <= m(c[0][col]) < upper_M:
            row_i = int((u_v[col] - MIN_Y) * DIVS[i] / (MAX_Y - MIN_Y))
            col_i = int((v_j[col] - MIN_X) * DIVS[i] / (MAX_X - MIN_X))
            if len(data) > row_i >= 0 and len(data[0]) > col_i >= 0:
                data[row_i][col_i].append(c[1][col] / c[0][col])
    avg_data = np.zeros((len(data), len(data[0])))
    for r in range(len(data)):
        for j in range(len(data[0])):
            if len(data[r][j]) != 0:
                avg_data[r][j] = len(data[r][j])
                #avg_data[r][j] = statistics.median(data[r][j])
    z.append(avg_data)

for i in range(Nr * Nc):
    for r in range(len(z[i])):
        for c in range(len(z[i][0])):
            if z[i][r][c] == 0:
                z[i][r][c] = np.nan

cmap = 'cool'
#vmin = 5 * 10 ** -12
#vmax = 5 * 10 ** -8
vmin = 0
vmax = 100
#norm = colors.LogNorm(vmin=vmin, vmax=vmax)
norm = colors.Normalize(vmin=vmin, vmax=vmax)

fig, axs = plt.subplots(Nr, Nc, sharex=True, sharey=True)

imgs = []

for row in range(Nr):
    for col in range(Nc):
        i = Nc * row + col
        imgs.append(axs[row][col].pcolormesh(x[i], y[i], z[i],
                                             cmap=cmap, norm=norm))
        axs[row][col].plot(x_arr, y_arr)
        axs[row][col].set_xlim([MIN_X, MAX_X])
        axs[row][col].set_ylim([MIN_Y, MAX_Y])

fig.text(0.445, 0.062, 'V - J', ha='center', va='center')
fig.text(0.06, 0.5, 'U - V', ha='center', va='center',
         rotation='vertical')
fig.text(0.9, 0.5, 'Density', ha='center', va='center',
         rotation='vertical')
'''
fig.text(0.195, 0.92, 'log(M) : 7 - 8', ha='center', va='center')
fig.text(0.400, 0.92, 'log(M) : 9 - 10', ha='center', va='center')
fig.text(0.605, 0.92, 'log(M) : 10 - 11', ha='center', va='center')
'''

min_x = 0.160
max_x = 0.715
for i in range(Nc):
    lower_M = i * (MAX_MASS - MIN_MASS) / Nc + MIN_MASS
    upper_M = lower_M + (MAX_MASS - MIN_MASS) / Nc
    fig.text(i * (max_x - min_x) / (Nc - 1) + min_x, 0.9, 'log(M) : {} - {}'.format(lower_M, upper_M),
             ha='center', va='center')

min_y = 0.049
max_y = 0.819
for i in range(Nr):
    lower_z = i * (MAX_Z - MIN_Z) / Nr + MIN_Z
    upper_z = lower_z + (MAX_Z - MIN_Z) / Nr
    fig.text(0.8, (Nr - i) * (max_y - min_y) / Nr + min_y, 'z : {} - {}'.format(str(lower_z)[:4], str(upper_z)[:4]),
             ha='center', va='center', rotation='vertical')

fig.colorbar(imgs[0], ax=axs, orientation='vertical', fraction=0.1)

fig.tight_layout(pad=0.5, rect=(0.05, 0.05, 0.79, 0.9))

plt.subplots_adjust(hspace=.0, wspace=.0)
plt.show()
