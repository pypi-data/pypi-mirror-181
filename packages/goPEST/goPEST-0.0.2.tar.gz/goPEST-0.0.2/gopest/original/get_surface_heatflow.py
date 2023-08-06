"""Get heatflow through the surface of the model
Need to have file "get_surface_heatflow.cfg" in the working directory
"""

"""
Potential problem - lst.history() is used, so I am not sure how it would
react to short output.  All lst.history() used here assumes the returned
times are identical, no checking is done.

To be checked - The way it calculates normalised heatflows is the same
as implemented in Mulgraph2.  All postive and negative heatflow are added
together.  Eylem is wondering if I can add feature that not counting these
flows from atmosphere into surface block.
"""

from config import *
from mulgrids import *
from t2listing import *
from numpy import array
import os.path
from os import getcwd

def wc_match(name_wc, name):
	""" return true if the name_wc (wild cast * supported) matches name """
	if len(name_wc) != len(name): return False
	is_match = True
	for i in xrange(len(name)):
		if name_wc[i] != '*':
			if name_wc[i] != name[i]:
				is_match = False
				break
	return is_match

def get_surface_heatflow_proc_cfg(cfg,geo=None,lst=None):
    # main options
    ListingTableNames = cfg.get_list('ListingTableNames')
    syear = float(cfg.get_value('HistoryStartingYear').strip())
    coldenthalpy = float(cfg.get_value('ColdWaterEnthalpy_J/kg').strip())
    incgeners = cfg.get_list('IncludeGENERs')
    # optional options
    show_fig, save_fig = False, False
    if cfg.check_optional('ShowPlots'):
        show_fig = 't' in cfg.get_value('ShowPlots').lower()
    if cfg.check_optional('SavePlots'):
        save_fig = 't' in cfg.get_value('SavePlots').lower()
    outflow_only = False
    if cfg.check_optional('OutflowOnly'):
        outflow_only = 't' in cfg.get_value('OutflowOnly').lower()
    calc_notinany = False
    if cfg.check_optional('NotInAny'):
        calc_notinany = 't' in cfg.get_value('NotInAny').lower()

    if geo is None:
        print ' Reading geometry file...'
        geo = mulgrid(cfg.get_value('GeometryFile').strip())
    if lst is None:
        print ' Reading listing file...'
        lst = t2listing(cfg.get_value('ListingFile').strip())

    # ensure there is atmosphere block in the model, if not, no surface heat flow
    # is possible, exit program
    if geo.atmosphere_type not in [0,1]:
        print ' ERROR: The model must have atmosphere block to allow surface heatflow.'
        exit()

    print ' Processing user defined zones...'
    colsinzones={}
    for s in cfg.get_list('UserDefinedZones_ColumnNames'):
        matched = []
        for wc_c in cfg.get_list(s.rstrip()):
            for c in geo.column.keys():
                if wc_match(wc_c,c) & (c not in matched):
                    matched.append(c)
        colsinzones[s.rstrip()]=[geo.column[x] for x in matched]
    for s in cfg.get_list('UserDefinedZones_Polygon'):
    	zone_polygon=[]
    	for pt in cfg.get_list(s.rstrip()):
    		(x,y) = eval(pt)
    		p = array([x,y])
    		zone_polygon.append(p)
    	colsinzones[s.rstrip()]=geo.columns_in_polygon(zone_polygon)

    if calc_notinany:
        allcols = []
        for z in colsinzones.keys():
            allcols = allcols + [c.name for c in colsinzones[z]]
        special = 'NOT_IN_ANY'
        if special not in colsinzones:
            colsinzones[special] = [c for c in geo.columnlist if c.name not in allcols]


    print ' Searching for included GENERs...'
    geners = []
    for g in incgeners:
        geners = geners + [(x,y) for x,y in lst.generation.row_name if wc_match(g.rstrip(),y)]

    print ' Generators specified:', geners

    return (geners,colsinzones,ListingTableNames,syear,coldenthalpy,
        show_fig,save_fig,outflow_only,calc_notinany)

def get_surface_heatflow(geo,lst,geners,colsinzones,
    ListingTableNames,syear,coldenthalpy,
    show_fig=False,save_fig=False,outflow_only=False,calc_notinany=False):
    """
        geners,colsinzones easier to obtain from get_surface_heatflow_proc_cfg()
    """
    [name_grate, name_enth, name_heatflow, name_massflow] = ListingTableNames

    # allcols may have repeated col names if user defined zones overlaps, but it
    # should be okay, as it's only used to avoid calculating heatflows from geners
    # that is not in any defined zones at all
    if not calc_notinany:
        allcols = []
        for z in colsinzones.keys():
            allcols = allcols + [c.name for c in colsinzones[z]]
    else:
        allcols = [c.name for c in geo.columnlist]

    print ' Calculating column heatflows from GENERS...'
    allgeners = []
    for b,g in geners:
        col_name = geo.column_name(b)
        if col_name in allcols:
            allgeners = allgeners + [('g',(b,g),name_grate),('g',(b,g),name_enth)]

    allgenermassheatflow = lst.history(allgeners)
    nrmhf_gener = {}
    for i in range(0,len(allgeners),2):
        (tr,rate),(te,enth) = allgenermassheatflow[i], allgenermassheatflow[i+1]
        (tmp,(b,g),tmp2) = allgeners[i]
        col_name = geo.column_name(b)
        if col_name in nrmhf_gener:
            nrmhf_gener[col_name] = nrmhf_gener[col_name] - rate * (enth - coldenthalpy)
        else:
            nrmhf_gener[col_name] = - rate * (enth - coldenthalpy)

    if show_fig or save_fig: import matplotlib.pyplot as plt

    print ' Calculating total surface heatflow for each zone...'
    print ' Results are given as Year, Total Heat Flow (W), Heat Flux (W/m^2):'
    print " --------------------"
    zone_total={}
    zone_area={}
    for zone in sorted(colsinzones.keys()):
        print ''
        print ' Zone:', zone, '-',colsinzones[zone]
        base,ext=os.path.splitext(lst.name)
        outfilename=base+'_SurfaceHeatFlow_'+zone+'.csv'
        outfile=file(outfilename,'w')
        outfile.write('Year, Total Heat Flow W, Heat Flux W/m^2\n')
        zone_total[zone] = [0.0]
        zone_area[zone] = 0.0
        allcolsinzone = []
        for col in colsinzones[zone]:
            lay = geo.layerlist[geo.num_layers-col.num_layers]
            layatm = geo.layerlist[0]
            blockname = geo.block_name(lay.name,col.name)
            if geo.atmosphere_type == 0:
                blocknameatm = geo.block_name(layatm.name,geo.atmosphere_column_name)
            else:
                blocknameatm = geo.block_name(layatm.name,col.name)
            allcolsinzone = allcolsinzone + [('c',(blockname,blocknameatm),name_heatflow),('c',(blockname,blocknameatm),name_massflow)]
            if col.name in nrmhf_gener:
                zone_total[zone] = zone_total[zone] + nrmhf_gener[col.name]
            zone_area[zone] = zone_area[zone] + col.area

        allmassheatflow = lst.history(allcolsinzone)
        for i in range(0,len(allcolsinzone),2):
            (t,hf),(t,mf) = allmassheatflow[i],allmassheatflow[i+1]

            # still not convinced this is good idea, check with Mike and Adrian
            # excluding if downflow
            if outflow_only:
                for ti,h in enumerate(hf):
                    if h > 0.0:
                        hf[ti],mf[ti] = 0.0,0.0

            # reverse the sign to become "outflow"
            zone_total[zone] = zone_total[zone] -(hf - mf * coldenthalpy)

        for (x,y,z) in zip(t/60.0/60.0/24.0/365.25+syear, zone_total[zone], zone_total[zone]/zone_area[zone]):
            print x,y,z
            line = str(x) +','+ str(y) +','+ str(z)+"\n"
            outfile.write(line)
        outfile.close()
        print " -> written to file: ", outfilename

        if show_fig or save_fig:
            ax = plt.subplot(111)
            ax.cla()
            ax.plot([x/60.0/60.0/24.0/365.25+syear for x in t], [y/1.0e6 for y in zone_total[zone]])
            ax.grid(True)
            ax.set_title(zone)
            ax.set_xlabel('Year')
            ax.set_ylabel('Heatflow MW')
            if show_fig: plt.show()
            if save_fig: plt.savefig(base+'_SurfaceHeatFlow_'+zone+'.png')

    print " --------------------"
    return t, zone_total, zone_area
    # t is np.array
    # zone_total, zone_area is dict of np.arrays, keys are the same as colsinzones


if __name__ == '__main__':
    cfg_name = os.path.split(__file__)[-1].split('.')[0] + '.cfg'
    cfg_name = os.getcwd() + os.path.sep + cfg_name
    cfg = config(cfg_name)

    print ' Reading geometry file...'
    geo = mulgrid(cfg.get_value('GeometryFile').strip())
    print ' Reading listing file...'
    lst = t2listing(cfg.get_value('ListingFile').strip())

    (geners,colsinzones,ListingTableNames,syear,coldenthalpy,
        show_fig,save_fig,outflow_only,calc_notinany
        ) = get_surface_heatflow_proc_cfg(cfg,geo,lst)

    get_surface_heatflow(geo,lst,geners,colsinzones,
        ListingTableNames,syear,coldenthalpy,
        show_fig,save_fig,outflow_only,calc_notinany)
