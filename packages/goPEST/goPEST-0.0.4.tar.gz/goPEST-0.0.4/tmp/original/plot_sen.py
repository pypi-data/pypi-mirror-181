"""
extract and plot sensitivity of parameters, with some statistics
"""

iterations = []

f = open('case_reg.sen')
line = f.readline()
while line:
    if line.strip().startswith('OPTIMISATION ITERATION NO.'):
        words = line.split()
        it = int(words[3])
        iterations.append([])
        print it

        line = f.readline()
        line = f.readline()
        while line.strip():
            words = line.split()
            # append (par name, group, value, sen)
            iterations[-1].append((words[0], words[1], float(words[2]), float(words[3])))
            line = f.readline()

    line = f.readline()

f.close()


def plot_sorted_sen(list_of_tuple, sort_idx=None, show_only=None):
    from matplotlib import pyplot as plt
    from operator import itemgetter
    import numpy as np
    if sort_idx:
        lot = sorted(list_of_tuple, key=itemgetter(sort_idx))
        if show_only:
            lot = lot[-show_only:]
    else:
        lot = list_of_tuple

    par, grp, val, sen = zip(*lot)
    ypos = np.arange(len(lot))
    plt.barh(ypos, sen)
    if show_only:
        plt.yticks(ypos, par)
    plt.xlabel('Sensitivity')
    plt.ylabel('Parameters')
    plt.show()

plot_sorted_sen(iterations[-1], 3, 50)


