from Constants.constants import *

new_contents = ''

file = '{}Constants/constants.py'.format(ROOT)
with open(file, 'r') as f:
    for line in f.readlines():
        if len(line.split()) > 0 and line.split()[0] == 'NGAL':
            idtempz_length = len(np.loadtxt('{}Extra/idtempz.txt'.format(ROOT)))
            new_contents += 'NGAL = {}\n'.format(idtempz_length)
        else:
            new_contents += line

with open(file, 'w') as f:
    f.write(new_contents)
