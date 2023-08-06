import glob
import sys
from os import remove

dry = '--dry' in sys.argv[1:]

if dry:
    print '--- dry run --- ',
print ' removing files:'

patterns = [
    'pest_model.dat.*',
    'pest_model.obf.*',
    'real_model.incon.*',
    # 'slurm*.out',
]

for pat in patterns:
    for f in glob.glob(pat):
        print f
        if not dry:
            remove(f)


