from goPESTpar import generate_real_model
import os

def get_pest_dir():
    with open('_pest_dir', 'r') as f:
        line = f.readlines()[0].strip()
        return line

TEMPCHEK = os.path.join(get_pest_dir(), 'tempchek')

if not os.path.isfile('case_reg.par'):
    print 'Error: file case_reg.par from optimisation is required.'
    exit()

os.system('%s pest_model.tpl pest_model.dat case_reg.par' % TEMPCHEK)

generate_real_model('real_model_original.dat', 'pest_model.dat', 'real_model.dat')


