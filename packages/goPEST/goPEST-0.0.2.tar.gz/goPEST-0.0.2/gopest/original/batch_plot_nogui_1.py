import time
START = time.time()

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np

from timgui.t2model import Model
from timgui.units import setTimeOffset, Unit

import os
import sys

def load_plot_list(fname, model):
    """ load the list of plots from json.  The returned object has nearly
    identical structure as the json file, apart from each series being loadded
    as one of the graph_dataseries objects. """
    import json
    f = open(fname,'r')
    jlist = json.load(f)
    f.close()

    import timgui.graph_dataseries as graph_dataseries
    plots = []
    for p in jlist:
        po = {'series':[]} # empty plot with empty series
        for s in p['series']:
            t = getattr(graph_dataseries, s['type'])
            del s['type']
            so = t(**s)
            so.connectModel(model)
            po['series'].append(so)
        del p['series']
        for k,v in p.iteritems():
            po[k] = v
        plots.append(po)

    return plots

# Not working?
def save_plot_list(fname, plots):
    """serialise the list of plots into file, allows later reload of the list"""
    def serialisePlot(plot):
        if not hasattr(plot, 'series'):
            return plot
        po = {}
        po['title'] = plot.title
        po['xlabel'] = plot.xlabel
        po['ylabel'] = plot.ylabel
        po['properties'] = plot.properties
        po['series'] = []
        for s in plot.series:
            so = {}
            so['type'] = s.__class__.__name__
            for k in s.KEYS:
                so[k] = getattr(s,k)
            po['series'].append(so)
        return po

    import json
    f = open(fname,'w')
    # NOTE, the self.plot_list.listObject() will be a normal sequence, so
    # the default encoding will treat it as normal list, and only call the
    # default at plot object level.  Hence serialisePlot only handles plot
    # instead of plot list.
    json.dump(plots, f, default=serialisePlot,
        indent=4, sort_keys=True)
    f.close()

def update_bounds(bounds, values):
    """ bounds can be a tuple of (min,max) or empty ().  The max/min will be
    updated by looking at values ( a list of values) """
    nlist = list(bounds) + list(values)
    return (min(nlist), max(nlist))

def calc_plot_lim(bounds, allow_neg=False):
    """ work out optimal lim to use for given bounds of values, used for
    pyplot.xlim()/ylim() """
    from math import modf
    # modf() gives (fractional, integer) parts of a float
    inc = 5.0

    diff = bounds[1] - bounds[0]
    mid = (bounds[1] + bounds[0]) / 2.0

    first = bounds[0] - modf(bounds[0]/inc)[0] * inc
    if (diff+inc) < 40.0:
        width = 40.0
    elif (diff+inc) < 60.0:
        width = 60.0
    elif (diff+inc) < 80.0:
        width = 80.0
    else:
        width = 100.0

    if mid < (first + width/2.0):
        while ((first + width - inc) > bounds[1]) and (mid < (first+width/2.0)):
            if ((first-inc) < 0.0) and (not allow_neg):
                break
            first -= inc
    else:
        while ((first+inc) < bounds[0]) and (mid >= (first+width/2.0)):
            first += inc
    return (first, first + width)

if __name__ == '__main__':
    # setTimeOffset('2009.63387978 year')
    setTimeOffset('1966.48 year')
    geo_name = 'g_real_model.dat'
    lst_names = [
        './original/real_model_pr.h5'
        ]
    fname = 'goPESTobs.json'
    OUTDIR = 'plots'
    try:
        os.mkdir(OUTDIR)
    except OSError:
        pass
    pdffname = os.path.splitext(fname)[0] + '.pdf'

    app = QApplication(sys.argv)

    model = Model()
    plots = load_plot_list(fname, model)

    model.loadFileMulgrid(geo_name)
    model.loadFileDataInput('real_model_pr.json')

    # freeze series if not FieldData for Frozen for each listing
    from timgui.graph_dataseries import FrozenDataSeries
    for lst in lst_names:
        model.loadFileT2listing(lst)
        for p in plots:
            saved_s = []
            for s in p['series']:
                if 'Field' not in s.__class__.__name__ and 'Frozen' not in s.__class__.__name__:
                    saved_s.append(FrozenDataSeries())
                    saved_s[-1].saveSeries(s)
                    saved_s[-1].name = ' '.join([str(s), lst])
            # only add to list after looping through
            p['series'] += saved_s

    # ofname = fname
    # if ofname.endswith('.json'):
    #     ofname = ofname[:-5]
    # save_plot_list(fname + '_.json', plots)

    # only plot Field and Frozen data series, ignore the rest
    from itertools import cycle
    pcnt = 0
    linespecs = ['co:', 'r^:', 'b+:', 'k*:', 'ms:', 'gx:']
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages
    pdf_pages = PdfPages(pdffname)
    for p in plots:
        # fig = plt.figure(figsize=(8.27, 11.69), dpi=100)
        fig = plt.figure(figsize=(3.1, 4.3), dpi=100)

        ls = cycle(linespecs)
        plt.clf()
        # plt.gcf().set_size_inches(14,9)
        plt.gcf().set_size_inches(14,9)
        plt.gcf().set_dpi(300)
        ybounds = ()
        for s in p['series'][::-1]:

            if 'Field' in s.__class__.__name__:
                # lbl = s.filename
                # lbl = os.path.split(s.filename)[-1]
                lbl = "Field Data"
            elif 'Frozen' in s.__class__.__name__:
                lbl = s.name
                # lbl = s.name.split()[-1]
                if 'best' in lbl:
                    lbl = 'Calibrated ' + lbl.split()[-1]
                elif 'original' in lbl:
                    lbl = 'Original ' + lbl.split()[-1]
                elif 'raw' in lbl.lower():
                    lbl = lbl
                else:
                    lbl = "PEST Obs " + lbl
            else:
                continue

            lss = ls.next()
            xs, ys = s.getXYData()

            if not isinstance(xs, np.ndarray):
                xs = np.array(xs)
            if not isinstance(ys, np.ndarray):
                ys = np.array(ys)
            if s.xunit == 't2sec':
                xs = (xs * Unit('t2sec')).to('year').magnitude
            if s.xunit == 't2year':
                xs = (xs * Unit('t2year')).to('year').magnitude
            if s.yunit in ['pascal', 'Pa']:
                ys = ys * Unit(s.yunit).to('bar').magnitude
                s.yunit = 'bar'
            if s.yunit == 'J/kg':
                ys = ys * Unit(s.yunit).to('kJ/kg').magnitude
                s.yunit = 'kJ/kg'

            # print(ys)
            print "%i >>> xunit = %10s; yunit = %10s" % (pcnt, str(s.xunit), str(s.yunit))

            ybounds = update_bounds(ybounds, ys)
            plt.plot(xs,ys,
                lss, mfc='none', mec=lss[0], ms=6.0, mew=1.0, lw=2.0, label=lbl)

        if 'enthalpy' in p['ylabel'].lower():
            p['ylabel'] = p['ylabel'] + ' (kJ/kg)'
        if 'pressure' in p['ylabel'].lower():
            p['ylabel'] = p['ylabel'] + ' (bar)'
        if 'temperature' in p['xlabel'].lower():
           p['xlabel'] = p['xlabel'] + ' (degC)'
        if 'time' in p['xlabel'].lower():
           p['xlabel'] = p['xlabel'] + ' (year)'
        if 'elevation' in p['ylabel'].lower():
           p['ylabel'] = p['ylabel'] + ' (mRL)'

        # plt.legend(loc='upper right')
        # Place a legend above this legend, expanding itself to
        # fully use the given bounding box.
        # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        #            ncol=2, mode="expand", borderaxespad=0.)
        # plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
        #            ncol=2)
        plt.legend(loc=0, ncol=1)
        plt.xlabel(str(p['xlabel']))
        plt.ylabel(str(p['ylabel']))
        plt.title(str(p['title']))
        if 'xlimit' in p:
            plt.xlim(tuple(p['xlimit']))
        if ('ylimit' in p):
            plt.ylim(tuple(p['ylimit']))
        else:
            if ('pressure diff' in p['ylabel'].lower()):
                plt.ylim(calc_plot_lim(ybounds, True))
            elif ('pressure' in p['ylabel'].lower()):
                plt.ylim(calc_plot_lim(ybounds))

        # plt.ylim(40.,70.)
        plt.grid(True)
        pcnt += 1; plt.savefig('%s/%i.eps' % (OUTDIR,pcnt))
        pdf_pages.savefig(fig)
        plt.close(fig)
        # del fig
    pdf_pages.close()


print 'Total walltime is', (time.time() - START), 'seconds'
