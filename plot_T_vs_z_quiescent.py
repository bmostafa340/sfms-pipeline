import matplotlib.pyplot as plt
from matplotlib import colors
from Constants.constants import *

MIN_X = 0
MIN_Y = 8
MAX_X = 6
MAX_Y = 60

DIVS = 53

dy = (MAX_Y - MIN_Y) / DIVS
dx = (MAX_X - MIN_X) / DIVS

y, x = np.mgrid[slice(MIN_Y, MAX_Y + dy, dy),
                slice(MIN_X, MAX_X + dx, dx)]

data = []
for r in range(len(y) - 1):
    data.append([])
    for _ in range(len(y[0]) - 1):
        data[r].append(0)

total = []
for i in range(len(data[0])):
    total.append(0)

file = '{}Computed_Files/galaxy_properties.npy'.format(ROOT)
props = np.load(file)[:, [1, 8]]

file = '{}Computed_Files/quiescent_idtemp_idxs.npy'.format(ROOT)
idxs = np.load(file)

#temps = props[:, 0]
#z = props[:, 1]

temps = props[idxs, 0]
z = props[idxs, 1]

del props

for i in range(len(temps)):
    x_val = z[i]
    y_val = temps[i]
    row = int((y_val - MIN_Y) * DIVS / (MAX_Y - MIN_Y))
    col = int((x_val - MIN_X) * DIVS / (MAX_X - MIN_X))
    if len(data) > row >= 0 and len(data[0]) > col >= 0:
        data[row][col] += 1
        total[col] += 1

for row in range(len(data)):
    for col in range(len(data[0])):
        if data[row][col] == 0:
            data[row][col] = np.nan
        else:
            data[row][col] /= total[col]

cmap = 'Reds'
vmin = 0
vmax = 15 / 100
norm = colors.Normalize(vmin=vmin, vmax=vmax)

fig, ax = plt.subplots()

plt.pcolormesh(x, y, data, cmap=cmap, norm=norm)
plt.colorbar()

plt.xlim(MIN_X, MAX_X)
plt.ylim(MIN_Y, MAX_Y)

plt.xlabel('z_phot')
plt.ylabel('Temperature [K]')

fig.text(0.88, 0.5, 'Density', ha='center', va='center',
         rotation='vertical')

plt.show()
