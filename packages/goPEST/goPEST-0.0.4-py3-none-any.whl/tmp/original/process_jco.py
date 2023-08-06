import numpy as np
import re
from pprint import pprint as pp

def read_jco_txt(fname):
    """ reads a text (use JCO2MAT) version of jcobian matrix into
    a numpy array, returns the data with rows of obs, cols of pars
    The row names, col_names also returned as lists.
    """
    with open(fname, 'r') as f:
        line = f.readline()
        n_obs, n_par, n = [int(i) for i in line.split()]
        
        # number of rows, cols, and (no idea what's the last)
        print "reading matrix file, with %i rows, %i columns..." % (n_obs, n_par)
        data = np.empty([n_obs, n_par])
        # put them into np.array
        for j in range(n_obs):
            d = []
            for i in range(n_par / 8 + 1):
                d += [float(x) for x in f.readline().strip().split()]
            data[j, :] = d
        
        # read row names (observations)
        line = f.readline()
        if line.strip() != '* row names':
            raise Exception
        row_names = []
        for j in range(n_obs):
            row_names.append(f.readline().strip())

        # read col names (parameters)
        line = f.readline()
        if line.strip() != '* column names':
            raise Exception
        col_names = []
        for i in range(n_par):
            col_names.append(f.readline().strip())
        return data, row_names, col_names
    
def get_matched_idx(str_list, patterns):
    import re
    rex = [re.compile(p) for p in patterns]
    idx = []
    for i,s in enumerate(str_list):
        if any(r.match(s) is not None for r in rex):
            idx.append(i)
    return idx

def write_csv(mat, obs, par, filename='jco.csv'):
    """
    Writes the JCO into a comma separated file (.csv), for easy
    post processing in Excel.  Row heading (observations) and 
    column heading (parameters) will be included.  
    """
    with open(filename, 'w') as f:
        f.write(',' + ','.join(par) + '\n')
        for i,s in enumerate(obs):
            f.write(s + ',')
            f.write(','.join([str(v) for v in mat[i,:]]))
            f.write('\n')
    
def reduce_jco(mat, obs, par, obs_only=['.+'], par_only=[',+']):
    """
    Reduce the JCO matrix to selected obs/par.  Selected obs/par
    is a list of names, with support of regular expression.

    Reduced mat, obs, par is returned as a tuple.
    """
    iobs = get_matched_idx(obs, obs_only)
    ipar = get_matched_idx(par, par_only)
    mat_reduced = mat[iobs, :][:, ipar]
    obs_reduced = [obs[ii] for ii in iobs]
    par_reduced = [par[ii] for ii in ipar]
    return mat_reduced, obs_reduced, par_reduced

def sum_jco_column(mat):
    """
    jco rows are observations
    jco cols are parameters
    sum column gives sensitivity of each parameters.
    """
    import numpy as np
    abs = np.absolute(mat)
    return np.sum(abs, axis=0)

if __name__ == '__main__':
    mat,obs,par = read_jco_txt('case_reg.jco.1.txt')

    pick_obs = [
        'ee_op3d_.+',
        'ee_op4d_.+',
        'ee_op5da_.+',
        'ee_op6d_.+',
        'ee_op7d_.+',
        'ee_pal11_.+',
        'ee_pal18_.+',
    ]
    pick_par = [
        'r1fbd03',
        'r2fbd03',
        'r3fbd03',
        'r3fbd09',
        'r3fbsa8',
        'r1fsd14',
        '.+',
    ]

    mat_r, obs_r, par_r = reduce_jco(mat, obs, par, 
        pick_obs, pick_par)

    write_csv(mat_r, obs_r, par_r, 'out2.csv')

    # find most important parameters for the specified 
    # observations (sum over obs for each par)
    mat_r, obs_r, par_r = reduce_jco(mat, obs, par, 
        pick_obs, ['.+'])
    sum = sum_jco_column(mat_r)
    order_par_i = np.argsort(sum)
    top_n = 20
    top_pars = [par[ii] for ii in order_par_i[::-1][:top_n]]
    top_pars_v = [sum[ii] for ii in order_par_i[::-1][:top_n]]
    
    pp(top_pars)

    # csv file with sum over each selected obs, to see most
    # important parameters over each group of enthalpies
    sums = []
    for pobs in pick_obs:
        mat_r, obs_r, par_r = reduce_jco(mat, obs, par, 
            [pobs], ['.+'])
        sums.append(sum_jco_column(mat_r))
    mat_r = np.vstack(tuple(sums))
    write_csv(mat_r, pick_obs, par, 'sum_group.csv')

