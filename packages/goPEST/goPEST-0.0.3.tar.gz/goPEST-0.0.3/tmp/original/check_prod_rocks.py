from mulgrids import *
from t2data import *

import json

def read_gener_file(fname):
    f = t2data_parser(fname,'rU')
    line = f.readline()
    if line[:5] <> 'GENER':
        # get rid of first line 'GENER' and check
        raise Exception("File %s is not a valid generator file, must starts with GENER." % fname)
    gs = t2data()
    gs.read_generators(f)
    f.close()
    return gs.generatorlist

def check(dat, geo):
    inj_rocks = []
    prd_rocks = []
    upf_rocks = []
    for g in dat.generatorlist:
        if g.type == 'MASS':
            if g.itab.strip():
                print g.name, dat.grid.block[g.block].rocktype
                if geo.layer_name(g.block) == geo.layerlist[-1].name:
                    print g.name, 'is upflow'
                    pass
                else:
                    inj_rocks.append(dat.grid.block[g.block].rocktype)
            else:
                if g.gx <= 0.0:
                    print '(p)', g.name, g.block, dat.grid.block[g.block].rocktype
                    prd_rocks.append(dat.grid.block[g.block].rocktype)
                else:
                    upf_rocks.append(dat.grid.block[g.block].rocktype)


    print 'injection', sorted(set(inj_rocks))
    print 'production', sorted(set(prd_rocks))
    print 'upflow', sorted(set(upf_rocks))

    print "'(%s)'" % ('|'.join(sorted([r.name for r in set(inj_rocks + prd_rocks + upf_rocks)])))


if __name__ == '__main__':
    dat = t2data('real_model_pr.dat')

    # production GENERs
    geners = read_gener_file('production.geners')

    # dict of gener (key) blocks (value)
    gener_block = dict([(g.name,g.block) for g in geners])
    # print gener_block

    # each Well's geners
    with open('data_well_geners.json', 'r') as f:
        well_geners = {}
        data = json.load(f)
        for k,v in data.iteritems():
            well_geners[k] = [gn for gn in v[1:-1].split('|')]

    for w in sorted(well_geners.keys()):
        print ('%10s' % w), ': ',
        bs, rs = [], []
        for g in well_geners[w]:
            r = dat.grid.block[gener_block[g]].rocktype.name
            print r,
        print '.'

