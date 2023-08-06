
from numpy.testing import assert_approx_equal
import os
import sys
import glob
from shutil import copy2
from itertools import izip

from goPESTpar import generate_real_model

def get_pest_dir():
    with open('_pest_dir', 'r') as f:
        line = f.readlines()[0].strip()
        return line

def get_master_dir():
    with open('_master_dir', 'r') as f:
        line = f.readlines()[0].strip()
        return line

def par_match(pf1, pf2):
    matched = False
    with open(pf1,'rU') as a:
        with open(pf2,'rU') as b:
            # once open successfully, assume equal, until something fails
            matched = True
            try:
                for aa,bb in izip(a,b):
                    ax, bx = float(aa.split(',')[0]), float(bb.split(',')[0])
                    assert_approx_equal(ax, bx, significant=7)
            except AssertionError:
                matched = False
    return matched

def usage():
    return '\n'.join([
        "    Convert a specified .par file into real_model using observation re-referencing.",
        ])

TEMPCHEK = os.path.join(get_pest_dir(), 'tempchek')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print usage()
        exit()
    par_file = sys.argv[1]
    if not os.path.isfile(par_file):
        print 'Error: PAR file %s does not exist.' % par_file
        print usage()
        exit()
    
    local = True
    if local:
        master_dir = '.'
    else:
        master_dir = get_master_dir()

    # use user specified .par file to create pest_model.dat
    os.system('%s pest_model.tpl pest_model.dat %s' % (TEMPCHEK, par_file))

    # obsreref: get matching incon, if exist
    if os.path.isfile('pest_model.obf'):
        os.remove('pest_model.obf')
    for parf in glob.glob(master_dir + os.sep + 'pest_model.dat.*'):
        print "---- checking %s ..." % parf
        if par_match(parf, 'pest_model.dat'):
            matchname = os.path.splitext(parf)[1]
            print "--- found matched incon/pars %s from master dir, overwrite Master INCON" % matchname
            copy2(master_dir + os.sep + 'real_model.incon' + matchname, master_dir + os.sep + 'real_model.incon')
            copy2(master_dir + os.sep + 'pest_model.obf' + matchname, 'pest_model.obf')
            break
    # print "--- remove all pairs from labmda tests after searching"
    # for f in glob.glob(master_dir + os.sep + 'pest_model.obf.*'):
    #     os.remove(f)
    # for f in glob.glob(master_dir + os.sep + 'pest_model.dat.*'):
    #     os.remove(f)
    # for f in glob.glob(master_dir + os.sep + 'real_model.incon.*'):
    #     os.remove(f)
    if os.path.isfile('pest_model.obf'):
        print "--- updated: pest_model.dat, pest_model.obf, real_model.incon"
    else:
        print "--- could not find matching pars"
        exit()

    # create real model using pest_model.dat
    generate_real_model('real_model_original.dat', 'pest_model.dat', 'real_model.dat')


