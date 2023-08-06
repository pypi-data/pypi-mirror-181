""" Passes the original model files (both NS and PR) through PyTOUGH and enable
extra-precision.  This will generate extra .pdat files from original models.
From this point and on, all later goPEST/PyTOUGH scripts will handle them
correctly and continue to use .pdat. """

from t2data import *
import re
import os

# set True to refresh values from .dat files, otherwise values in .pdat is used
clean_pdat = True

models = [
    'real_model_original.dat',
    'real_model_original_sp.dat',
    'real_model_original_dp.dat',
    'real_model_original_pr.dat',
    'real_model.dat',
    'real_model_pr.dat',
    ]

for f in models:
    if clean_pdat:
        pdat = re.sub(r'\.dat$', r'.pdat', f)
        print "removing file %s" % pdat
        if os.path.exists(pdat):
            os.remove(pdat)
    if os.path.exists(f):
        dat = t2data(f)
        dat.write(extra_precision=True, echo_extra_precision=True)
        del dat
        print "Model: %s turned on extra precision now." % f


