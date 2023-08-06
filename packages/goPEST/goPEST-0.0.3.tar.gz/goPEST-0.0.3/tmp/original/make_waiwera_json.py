from mulgrids import *
from t2data import *
from t2incons import *

import deepdiff
import h5py

import json

geo = mulgrid('g_real_model.dat')
dat = t2data('real_model.dat')
inc = t2incon('real_model.incon')

# check incon
inc_h5 = h5py.File('real_model.incon.h5', 'r')
inc_idx = len(inc_h5['time'][:,0]) - 1
if inc_idx < 0:
    raise Exception("ERROR! Waiwera initial conditions file 'real_model.incon.h5' has no data.")
inc_h5.close()

wdat_orig = json.load(open('real_model_original.json', 'r'))
# json.dump(wdat_orig, open('real_model_original.json', 'w'), indent=2, sort_keys=True)
wdat = dat.json(geo, 'g_real_model.msh',
                atmos_volume=1.e25,
                incons='prev.h5',
                eos=None,
                bdy_incons=inc, # somehow I still need it to avoid error
                mesh_coords='xyz')

# only need to update the generators/rocktypes, leave others as original
for k in ["source", "rock"]:
    wdat_orig[k] = wdat[k]

# overwrite these just to be safe
wdat_orig["thermodynamics"] = {"name": "ifc67", "extrapolate": True}
wdat_orig["initial"] = {"filename": "real_model.incon.h5", "index": inc_idx}
wdat_orig["output"]["filename"] = "real_model.h5"


json.dump(wdat_orig, open('real_model.json', 'w'), indent=2, sort_keys=True)


diff = deepdiff.DeepDiff(json.load(open('real_model_original.json', 'r')),
                         json.load(open('real_model.json', 'r')),
                         view='tree')

