import os
import shutil

flist = [
    ('real_model.dat', 'real_model.dat'),
    ('real_model.pdat', 'real_model.pdat'),
    ('real_model.listing', 'real_model.listing'),
    ('real_model.incon', 'real_model.incon'),
    ('real_model.save', 'real_model.save'),
    ('real_model_pr.dat', 'real_model_pr.dat'),
    ('real_model_pr.pdat', 'real_model_pr.pdat'),
    ('real_model_pr.dat', 'real_model_pr.dat'),
    ('real_model_pr.listing', 'real_model_pr.listing'),
    ('real_model_pr.incon', 'real_model_pr.incon'),
    ('real_model_pr.save', 'real_model_pr.save'),
]

for ff,ft in flist:
    fff, ttt = ('./%s' % ff), ('./best/%s' % ft)
    shutil.copy(fff, ttt)
    print 'copy file "%s" to "%s"' % (fff, ttt)

