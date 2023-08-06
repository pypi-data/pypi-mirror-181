import os
import shutil

flist = [
    ('real_model.dat', 'real_model_original.dat'),
    ('real_model.incon', 'real_model_original.incon'),
    ('real_model.dat', 'real_model.dat'),
    ('real_model.incon', 'real_model.incon'),
    ('real_model_pr.dat', 'real_model_original_pr.dat'),
]

for ff,ft in flist:
    fff, ttt = ('./original/%s' % ff), ('./%s' % ft)
    shutil.copy(fff, ttt)
    print 'copy file "%s" to "%s"' % (fff, ttt)

os.system('python make_enable_extra_precision.py')
