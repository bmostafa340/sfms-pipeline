from Constants.constants import *

orig_param = '{}Extra/param'.format(ROOT)
templates_replacement = '{}Extra/fspstemplates/'.format(ROOT)
catalog_replacement = '{}Computed_Files/Catalogs_By_Temp/COSMOS2015_'.format(ROOT)
res_replacement = '{}Extra/FILTER.RES.latest'.format(ROOT)

with open(orig_param, 'r') as f:
    orig_lines = f.readlines()

for temp in TEMPS:
    new_param = '{}Extra/Param_Files/param{}'.format(ROOT, temp)
    with open(new_param, 'w') as f:
        for line in orig_lines:
            split = line.split()
            if split[0] == 'TEMPLATES_FILE':
                path = '{0}{1}k/{1}k.spectra.param'.format(templates_replacement, temp)
                f.write('{}            {}\n'.format(split[0], path))
            elif split[0] == 'CATALOG_FILE':
                path = '{}{}K.fits'.format(catalog_replacement, temp)
                f.write('{}              {}\n'.format(split[0], path))
            elif split[0] == 'FILTERS_RES':
                f.write('{}               {}\n'.format(split[0], res_replacement))
            else:
                f.write(line)
