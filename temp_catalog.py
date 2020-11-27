from Constants.constants import *
from astropy.table import Table

file = '{}Extra/2015catalog.cat'.format(ROOT)

with open(file, 'r') as f:
    names = ['id', 'z_spec'] + f.readline().split()[2:]

arr = np.loadtxt(file, skiprows=1)

full_cat = {}
for line in arr:
    full_cat[line[0]] = line[1:]

del arr

cat_data = []
for temp in TEMPS:
    cat_data.append([])

file = '{}Extra/idtempz.txt'.format(ROOT)
idtemp = np.loadtxt(file)[:, [0, 1, 2]]

for arr in idtemp:
    ID = arr[0]
    temp = int(arr[1])
    z = arr[2]
    table = cat_data[TEMP_IDXS.get(temp)]
    data = [ID, z] + list(full_cat.get(ID))
    table.append(data)

del idtemp
del full_cat

for temp in TEMPS:
    table = np.array(cat_data[TEMP_IDXS.get(temp)])
    file = '{}Computed_Files/Catalogs_By_Temp/COSMOS2015_{}K'.format(ROOT, temp)
    with open(file, 'w') as f:
        f.write('# id\n')
        for col in range(len(table)):
            f.write('{}\n'.format(int(table[col][0])))
    table = Table(table, names=names, dtype=[float] * len(names))
    table.write('{}Computed_Files/Catalogs_By_Temp/'
                'COSMOS2015_{}K.fits'.format(ROOT, temp), overwrite=True)
