from Constants.constants import *
import os

templates_path = '{}Extra/fspstemplates/'.format(ROOT)

files = []
for temp in range(8, 61):
    file1 = '{0}{1}k/{1}k.spectra.param'.format(templates_path, temp)
    file2 = '{}{}k/template_'.format(templates_path, temp)
    if os.path.isfile(file1):
        os.remove(file1)
    with open(file1, 'w') as f:
        for i in range(1, 12):
            f.write('{} {}{} 1.0 0.0 1.0\n'.format(i, file2, i-1))
        f.write('12 {}11 1.0 0.0 1.0'.format(file2))
