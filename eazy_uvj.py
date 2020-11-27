from Constants.constants import *
import eazy

for temp in TEMPS
    print(temp)
    uvj_fluxes = []
    cat = '{}Computed_Files/Catalogs_By_Temp/COSMOS2015_{}K'.format(ROOT, temp)
    with open(cat, 'r') as f:
        f.readline()
        if not f.readline():
            np.save('{}Computed_Files/UVJ_By_Temp/{}'.format(ROOT, temp), uvj_fluxes)
            continue
    param_file = '{}Extra/Param_Files/param{}'.format(ROOT, temp)
    translate_file = '{}Extra/new_2015_translate.translate'.format(ROOT)
    photoz = eazy.photoz.PhotoZ(param_file=param_file, translate_file=translate_file, zeropoint_file=None,
                                load_prior=False, load_products=False)
    photoz.fit_parallel(photoz.idx, n_proc=4)
    fluxes = photoz.rest_frame_fluxes(percentiles=[50])[1]
    cat = '{}Computed_Files/Catalogs_By_Temp/COSMOS2015_{}K'.format(ROOT, temp)
    ids = np.loadtxt(cat, skiprows=1)
    for i, ID in enumerate(ids):
        u_flux = fluxes[i][0][0]
        v_flux = fluxes[i][2][0]
        j_flux = fluxes[i][3][0]
        log_u = -np.log(u_flux) / np.log(2.512)
        log_v = -np.log(v_flux) / np.log(2.512)
        log_j = -np.log(j_flux) / np.log(2.512)
        u_v = log_u - log_v
        v_j = log_v - log_j
        uvj_fluxes.append([ID, u_v, v_j])
    np.save('{}Computed_Files/UVJ_By_Temp/{}'.format(ROOT, temp), uvj_fluxes)
