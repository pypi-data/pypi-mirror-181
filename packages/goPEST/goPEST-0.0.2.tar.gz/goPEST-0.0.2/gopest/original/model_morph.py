"""
The idea is to help the convegence of model when the difference between two
model are too big for the save file to be used by the other as initial
condition.  It basically breaks down the (big) differences into many steps
(intermediate models) of smaller changes, so that each model step can converge
easily.

Use:


It seems to be hard to generalise this if the difference between two models
includes things such as rock assignments or addition/removing of generators.  So
here it stayed in a simple form of values changing.
"""

from t2data import *
from t2incons import *

import time

def make_intermediate_model(dat_from, dat_to, dat_middle, portion):
    """ portion should be between 0.0 and 1.0.  dat_from is where the model
    starts, which incon converges well.  dat_to is the final model.  dat_middle
    will be set with values calculated using the portion of overall changes.

    It is assumed the number/order of rock types and generators areidentical
    among the three model objects.  Only values are different.
    """
    from math import log10, pow

    if portion > 1.0 or portion < 0.0:
        raise Exception("A portion between 0.0 and 1.0 must be used.")

    for rf, rt, rm in zip(dat_from.grid.rocktypelist,
                          dat_to.grid.rocktypelist,
                          dat_middle.grid.rocktypelist):
        for i in range(3):
            logkf, logkt = log10(rf.permeability[i]), log10(rt.permeability[i])
            rm.permeability[i] = pow(10.0, logkf+(logkt-logkf)*portion)
        rm.porosity = rf.porosity + (rt.porosity - rf.porosity) * portion

    for gf, gt, gm in zip(dat_from.generatorlist,
                          dat_to.generatorlist,
                          dat_middle.generatorlist):
        if (gf.type=='MASS') and (gf.gx >= 0.0):
            gm.gx = gf.gx + (gt.gx - gf.gx) * portion
            gm.ex = gf.ex + (gt.ex - gf.ex) * portion

    return

def reset_incon_file(f):
    inc = t2incon(f + '.save')


    if 'sumtim' in inc.timing:
        with open("model_morph.log", "a") as mlog:
            mlog.write('    sumtim (ST) is %e sec\n' % inc.timing['sumtim'])

    inc.porosity = None
    inc.write(f + '.incon', reset=True)

def main(f_from, f_to, n):
    from os.path import splitext, basename
    datbase, ext = splitext(f_to)
    tmp_name = datbase + '_tmp'

    inc_from = splitext(f_from)[0] + ".incon"
    inc = t2incon(inc_from)
    inc.porosity = None
    inc.write(tmp_name + ".incon", reset=True)

    dat_from = t2data(f_from)
    dat_to = t2data(f_to)
    dat_middle = t2data(f_from)

    global PREV_TIME
    # reset log
    with open("model_morph.log", "w") as mlog:
        mlog.write('')

    ps = [float(i+1)/float(n) for i in range(n)]
    for portion in ps:
        make_intermediate_model(dat_from, dat_to, dat_middle, portion)

        # additional param etc
        dat_middle.parameter['max_timesteps'] = 500
        dat_middle.parameter['print_interval'] = 500
        dat_middle.parameter['tstop'] = 1.0E15

        dat_middle.write(tmp_name + ext, echo_extra_precision=True)

        # RUN!
        PREV_TIME = time.time()
        dat_middle.run(simulator="AUTOUGH2_3D") # AUTOUGH2_5Dbeta
        with open("model_morph.log", "a") as mlog:
            mlog.write('Portion %f completed after %.2f sec\n' % (portion, time.time() - PREV_TIME))

        reset_incon_file(tmp_name)

if __name__ == '__main__':
    main('real_model_original.dat', 'real_model.dat', 20)



