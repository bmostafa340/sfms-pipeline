from Constants.constants import *
import numpy as np
import statistics
import matplotlib.pyplot as plt
from matplotlib import colors
from astropy.cosmology import FlatLambdaCDM
import astropy.units as u


def line(B, x):
    return B[0] * x + B[1]


def m(val):
    return np.log10(val)


MIN_X = 5
MIN_Y = -3
MAX_X = 12
MAX_Y = 4

COSMO = FlatLambdaCDM(H0=70 * u.km / u.s / u.Mpc, Tcmb0=2.725 * u.K, Om0=0.3)

DIVS = []
for i in range(Nr * Nc):
    DIVS.append(20)

dx, dy = [], []
for i in range(Nr * Nc):
    dy_i = (MAX_Y - MIN_Y) / DIVS[i]
    dx_i = (MAX_X - MIN_X) / DIVS[i]
    dy.append(dy_i)
    dx.append(dx_i)

y, x = [], []
for i in range(Nr * Nc):
    y_i, x_i = np.mgrid[slice(MIN_Y, MAX_Y + dy[i], dy[i]),
                        slice(MIN_X, MAX_X + dx[i], dx[i])]
    x.append(x_i)
    y.append(y_i)

file = '{}Computed_Files/galaxy_properties.npy'.format(ROOT)
c = np.load(file)
c = c[:, [1, 2, 3, 8]].transpose()

z = []
pts = []

idxs = np.load('{}Computed_Files/sf_idtemp_idxs.npy'.format(ROOT))

for i in range(Nr * Nc):
    lower_z = i / (Nr * Nc) * (MAX_Z - MIN_Z) + MIN_Z
    upper_z = lower_z + 1 / (Nr * Nc) * (MAX_Z - MIN_Z)
    data = []
    for r in range(len(y[i]) - 1):
        data.append([])
        for _ in range(len(y[i][0]) - 1):
            data[r].append([])
    pts.append([[], []])
    for col in idxs:
        if lower_z <= c[3][col] < upper_z and c[1][col] > 0 and c[2][col] > 0:
            x_val = m(c[1][col])
            y_val = m(c[2][col])
            row_i = int((y_val - MIN_Y) * DIVS[i] / (MAX_Y - MIN_Y))
            col_i = int((x_val - MIN_X) * DIVS[i] / (MAX_X - MIN_X))
            if len(data) > row_i >= 0 and len(data[0]) > col_i >= 0:
                pts[i][0].append(x_val)
                pts[i][1].append(y_val)
                data[row_i][col_i].append(c[0][col])
    avg_data = np.zeros((len(data), len(data[0])))
    for r in range(len(data)):
        for j in range(len(data[0])):
            if len(data[r][j]) > 0:
                avg_data[r][j] = int(statistics.median(data[r][j]))
    z.append(avg_data)

for i in range(Nr * Nc):
    for r in range(len(z[i])):
        for c in range(len(z[i][0])):
            if z[i][r][c] == 0:
                z[i][r][c] = np.nan

cmap = 'jet'
vmin = 15
vmax = 50
norm = colors.Normalize(vmin=vmin, vmax=vmax)

fig, axs = plt.subplots(Nr, Nc, sharex=True, sharey=True)

imgs = []
domain = []
for i in range(Nr * Nc):
    domain.append((5, 12))

coeffs = []
for row in range(Nr):
    for col in range(Nc):
        i = Nc * row + col
        imgs.append(axs[row][col].pcolormesh(x[i], y[i], z[i], cmap=cmap,
                                             norm=norm))
        '''
        D_TIME = (MAX_Z - MIN_Z) / (Nr * Nc)
        min_z = i * D_TIME
        max_z = (i + 1) * D_TIME
        avg_z = (min_z + max_z) / 2
        age = COSMO.age(avg_z).value
        m = line([0.01255472, 0.8407227], age)
        c = line([-0.07796152, 0.05852118], age) - 8 * m
        coeff = np.array([m, c])
        fit_x = [MIN_X, MAX_X]
        fit_y = line(coeff, np.array(fit_x))
        axs[row][col].plot(fit_x, fit_y)
        '''
        '''
        coeff = np.polyfit(pts[i][0], pts[i][1], 1)
        linear = regression.Model(line)
        mydata = regression.Data(pts[i][0], pts[i][1])
        myodr = regression.ODR(mydata, linear, beta0=coeff)
        coeff = myodr.run().beta
        coeffs.append(coeff)
        fit_x = [MIN_X, MAX_X]
        fit_y = line(coeff, np.array(fit_x))
        axs[row][col].plot(fit_x, fit_y)
        '''
        axs[row][col].set_xlim([MIN_X, MAX_X])
        axs[row][col].set_ylim([MIN_Y, MAX_Y])
fig.text(0.04, 0.46, 'log(SFR)', ha='center', va='center',
         rotation='vertical')
fig.text(0.52, 0.05, 'log(M)', ha='center', va='center')
fig.text(0.5, 0.9, 'Temperature [K]', ha='center', va='center')

lower_x = 0.15
upper_y = 0.76
x_wid = 0.843
y_wid = 0.678
for i in range(Nr * Nc):
    lower_z = i / (Nr * Nc) * (MAX_Z - MIN_Z) + MIN_Z
    upper_z = lower_z + 1 / (Nr * Nc) * (MAX_Z - MIN_Z)
    lower_z = str(lower_z)[:4]
    upper_z = str(upper_z)[:4]
    fig.text(lower_x + (x_wid / Nc) * (i % Nc),
             upper_y - (y_wid / Nr) * int(i / Nc),
             'z : {} - {}'.format(lower_z, upper_z),
             ha='center', va='center')

    '''
    lower_z = i / (Nr * Nc) * MAX_Z
    upper_z = (i + 1) / (Nr * Nc) * MAX_Z
    fig.text(lower_x + (x_wid / Nc) * (i % Nc),
             upper_y - (y_wid / Nr) * int(i / Nc),
             'z : {} - {}\nbeta : {}, {}'.format(lower_z, upper_z,
                str(coeffs[i][0])[:5], str(coeffs[i][1])[:5]),
             ha='center', va='center')
    '''

cbaxes = fig.add_axes([0.05, 0.85, 0.9, 0.03])
fig.colorbar(imgs[0], cax=cbaxes, orientation='horizontal')

fig.tight_layout(pad=0.5, rect=(0.02, 0.04, 0.95, 0.8))

plt.subplots_adjust(hspace=.0, wspace=.0)
plt.show()
