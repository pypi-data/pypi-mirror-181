from tempfile import NamedTemporaryFile
from shutil import copy, move
import re
import os

def gen_file(filename, lines):
    if isinstance(lines, list):
        text = "\n".join(lines)
    else:
        # assume just plain text
        text = lines
    with open(filename, 'w') as f:
        f.write(text)

if os.name == 'posix':
    gen_file('model.bat', [
             '#!/bin/sh',
             'python submit_beopest.py --forward3 "python pest_model.py --test-update"',
             '# use the following for running PEST locally with NOPTMAX=0 for eg. /hpstart',
             '# export PATH=$PATH:./',
             '# python pest_model.py --local --skip-run',
             ])
    gen_file('d_model.bat', ['#!/bin/sh', 'python submit_beopest.py --forward3 "python pest_model.py"'])
    gen_file('r_model.bat', ['#!/bin/sh', 'python submit_beopest.py --forward3 "python pest_model.py --obsreref"'])

    gen_file('svdabatch.bat', ['#!/bin/sh', 'python submit_beopest.py --forward3 "python pest_model.py --svda --test-update"'])
    gen_file('d_svdabatch.bat', ['#!/bin/sh', 'python submit_beopest.py --forward3 "python pest_model.py --svda"'])
    gen_file('r_svdabatch.bat', ['#!/bin/sh', 'python submit_beopest.py --forward3 "python pest_model.py --svda --obsreref"'])
elif os.name == 'nt':
    gen_file('model.bat', [
             'python pest_model.py --test-update',
             'rem python pest_model.py --local --skip-run',
             ])
    gen_file('d_model.bat', 'python pest_model.py')
    gen_file('r_model.bat', 'python pest_model.py --obsreref')

    gen_file('svdabatch.bat', 'python pest_model.py --svda --test-update')
    gen_file('d_svdabatch.bat', 'python pest_model.py --svda')
    gen_file('r_svdabatch.bat', 'python pest_model.py --svda --obsreref')
else:
    print "os.name", os.name, "not recognised, don't know what to do."

print "removing ./ of svdabatch.bat from file case_svda.pst, please check."
with NamedTemporaryFile(delete=False) as tmp_sources:
    with open('case_svda.pst', 'rU') as sources_file:
        for line in sources_file:
            tmp_sources.write(re.sub(r'^( *)\.\/(svdabatch.bat)', r'\1\2', line))

move(tmp_sources.name, sources_file.name)

