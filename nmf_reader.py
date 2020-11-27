from Constants.constants import *
import numpy as np
import os

NMF_PROPS = '{}Extra/NMF_Props/'.format(ROOT)
NMF_RESTF = '{}Extra/NMF_RestF/'.format(ROOT)

ROOT = '/home/basel/Dropbox/hagan(1)/eazy-photoz-master/1K_Templates/'

PROPS = ['mass', 'sfr', 'age', 'Av', 'zmet', 'Lv']
RESTF = ['restU', 'restB', 'restV', 'restJ']
END = 'agn_tau'

for temp in TEMPS:
    dir_name = ROOT + 'nmf_{}K/'.format(temp)
    files = os.listdir(dir_name)
    files.sort()
    props_arr = np.zeros((560, len(PROPS)))
    restf_arr = np.zeros((560, len(RESTF)))
    idx = 0
    for filename in files:
        with open(dir_name + filename, 'r') as f:
            while True:
                line = f.readline().split()
                if len(line) < 2:
                    continue
                prop = line[1]
                if prop in PROPS:
                    props_arr[idx][PROPS.index(prop)] = float(line[3])
                elif prop in RESTF:
                    restf_arr[idx][RESTF.index(prop)] = float(line[3])
                if prop == END:
                    break
        idx += 1
    file = NMF_PROPS + str(temp)
    with open(file, 'w') as f:
        f.write('# ')
        for prop in PROPS:
            f.write(prop + ' ')
        f.write('\n')
        for row in range(560):
            for col in range(len(PROPS)):
                f.write(str(props_arr[row][col]) + ' ')
            f.write('\n')
    file = NMF_RESTF + str(temp)
    with open(file, 'w') as f:
        f.write('# ')
        for prop in RESTF:
            f.write(prop + ' ')
        f.write('\n')
        for row in range(560):
            for col in range(len(RESTF)):
                f.write(str(restf_arr[row][col]) + ' ')
            f.write('\n')
