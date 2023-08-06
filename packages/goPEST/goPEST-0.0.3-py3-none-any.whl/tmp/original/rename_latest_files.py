import glob
import os
from shutil import copy2

def current_iteration():
    its = [int(f.split('.')[-1]) for f in glob.glob('case_reg.jco.*')]
    its.append(0)
    return max(its)

if __name__ == '__main__':
    """ PEST_HP's file distribution will copy files from the best update slave
    to here.  They will be named as '*.999'.  This script renames these to the
    latest iteration number.
    """
    print 'rename_latest_files.py:'

    try:
        copy2('real_model.incon.999', 'real_model.incon')
        print "    real_model.incon.999 -> real_model.incon (copy)"
    except Exception as e:
        print " ", e
        print "  failed to copy incon file for next iteration!"

    ii = current_iteration()
    print '  Current iteration is %i' % ii

    for f in glob.glob('*.999'):
        newname = f.replace('.999', '.%i' % ii)
        print '    %s -> %s' % (f, newname)
        try:
            os.rename(f, newname)
        except Exception as e:
            print e
