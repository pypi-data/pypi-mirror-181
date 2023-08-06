"""
extract and plot lambda vs phi reduction at each iteration from PEST .rec files
"""

from math import log10


def plot_lambda_reduction(lams, reds, it_num):
    from matplotlib import pyplot as plt
    from operator import itemgetter
    if len(lams) == 0:
        return
    x, y = zip(*sorted(zip(lams, reds), key=itemgetter(0)))
    xe, ye = [x[0], x[-1]], [1.0, 1.0]
    plt.semilogx(x, y, 'b-+', xe, ye, 'r-')
    plt.title('ITERATION NO. %i' % it_num)
    plt.xlabel('lambda (log10)')
    plt.ylabel('Phi reduction')
    plt.gcf().savefig('phi_lambda_it%02i.png' % it_num)
    # plt.show()
    plt.gcf().clear()

f = open('case_reg.rec', 'r')

its = []

line = f.readline()
while line:
    if line.strip().startswith('OPTIMISATION ITERATION NO.'):
        if len(its) > 0:
            # plot prev iteration
            plot_lambda_reduction(its[-1][0], its[-1][1], it)

        words = line.split(':')
        it = int(words[1])
        its.append([[],[]])
        # print it

    if line.strip().startswith('Lambda = '):
        words = line.split()
        lam = float(words[2])

        line = f.readline()
        if not 'cannot be calculated' in line:
            words = line.split()
            red = float(words[4])
            its[-1][0].append((lam))
            its[-1][1].append((red))
            # print log10(lam), red


    line = f.readline()

f.close()