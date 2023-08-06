from mulgrids import *

with open('goPESTobs.coverage','r') as f:
    coverage = eval(f.read())
    

f.close()

geo = mulgrid('g_real_model.dat')

layers = geo.layerlist
blocks = geo.block_name_list
blockvars = [0]*len(blocks)


coveredtemps = []
for keys in coverage.keys():
    if ('temp' in keys and 'interp' not in keys):
        coveredtemps.extend(coverage[keys])

        
for blk in coveredtemps:
    if blk in blocks:
        for layer in geo.layerlist:
            if blk[3:] in layer.name:
                thickness = layer.thickness
                break
            else:
                thickness = 0
        blockvars[blocks.index(blk[:3] + geo.layerlist[-1].name)] += thickness #layer thickness
            
var = [geo.column[b[:3]].surface for b in geo.block_name_list]


geo.layer_plot(geo.layerlist[-1], variable=blockvars, wells=True, colourmap='Reds')
