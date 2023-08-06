from t2data import *
import json

dat = t2data('real_model_original.dat')
mass, ratio = {}, {}
for g in dat.generatorlist:
    if g.block.endswith('61') and g.name.endswith('77') and g.type == 'MASS':
        mass[g.block] = g.gx
for g in dat.generatorlist:
    if g.block.endswith('61') and g.name.endswith('66') and g.type == 'COM2':
        ratio[g.block] = g.gx / mass[g.block]

with open('data_co2_ratio.json', 'w') as f:
    json.dump(ratio, f, indent=2, sort_keys=True)
