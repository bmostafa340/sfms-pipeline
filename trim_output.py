from Constants.constants import *

for temp in TEMPS:
    with open('{}OUTPUT_Full/photz_{}k.zout'.format(ROOT, temp), 'r') as read:
        with open('{}OUTPUT/photz_{}k.zout'.format(ROOT, temp), 'w') as write:
            for i in range(2000):
                write.write(read.readline())
