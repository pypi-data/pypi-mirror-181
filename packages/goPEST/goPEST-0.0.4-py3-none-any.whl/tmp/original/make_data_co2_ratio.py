""" extract the specified CO2 to mass ratio for upflows, for each column
"""

from t2data import *
import json

dat = t2data('real_model_original.dat')
mass, co2 = {}, {}
for g in dat.generatorlist:
    if g.block.endswith('61') and g.name.endswith('77') and g.type == 'MASS':
        mass[g.block] = g.gx
    if g.block.endswith('61') and g.name.endswith('66') and g.type == 'COM2':
        co2[g.block] = g.gx
ratio = {}
for b in co2.keys():
    if b not in mass:
        print('WARNING! Block %s has COM2 but no MASS gener!' % b)
    ratio[b] = co2[b] / mass[b]
    del mass[b]
for b in mass.keys():
    print('WARNING! Block %s has MASS but no COM2 gener!' % b)


with open('data_co2_ratio.json', 'w') as f:
    json.dump(ratio, f, indent=4, sort_keys=True)
