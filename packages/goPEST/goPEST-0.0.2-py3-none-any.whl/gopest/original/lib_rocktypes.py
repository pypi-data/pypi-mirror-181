def rockname_to_vals(rocknamelist,onlyshowrocks=None,rockgroup=None):
    """ setup rocktype values for color plots, either layer or slice.  
    rocknamelist is a list of names (eg. given as the order of blocks in 
    a slice plot.  will return a list of values smae length as rocknamelist, 
    contains indices of the second returned list of rockname (grouped and 
    sorted) if onlyshowrocks is provided as a list of either index or 
    name strings, rocknames outside this list will be given a vlaue of -1.
    if rockgroup is provided, the grouping will be applied. """
    if onlyshowrocks:
        if isinstance(onlyshowrocks[0],int):
            rocknames = [rocknamelist[irock] for irock in onlyshowrocks]
        else:
            rocknames = onlyshowrocks
    else:
        rocknames = rocknamelist

    if rockgroup:
        if isinstance(rockgroup,str): rockgroup = [i for i,c in enumerate(rockgroup) if c<>'*']
        def namegroup(name): return ''.join([c if i in rockgroup else '*' for i,c in enumerate(name)])
        rocknames = [namegroup(name) for name in rocknames]

    rocknames = list(set(rocknames))
    rocknames.sort()
    rockmap = dict(zip(rocknames, range(len(rocknames))))

    if rockgroup:
        vals = []
        for name in rocknamelist:
            if namegroup(name) in rockmap:
                vals.append(rockmap[namegroup(name)])
            else:
                vals.append(-1)
    else:
        vals = [rockmap[name] for name in rocknamelist]
    return vals,rocknames

def update_rocktype_bycopy(dat, blk_names, to_rocktype, convention='++***'):
    """ 
        this copies the rocktype onto blocks in blk_names, if need new rocktype 
        names, part of the name can be preserved, the rest copied.
        to_rocktype has to be a PyTOUGH 'rocktype' object 
    """
    for b in blk_names:
        r_name = ''
        for i,c in enumerate(convention):
            if c == '+':
                r_name = r_name + dat.grid.block[b].rocktype.name[i]
            else:
                r_name = r_name + to_rocktype.name[i]
        if r_name not in dat.grid.rocktype:
            from copy import deepcopy
            new_rock = deepcopy(to_rocktype)
            new_rock.name = r_name
            
            # THIS IS ONLY FOR EMILY AND ME, DANGEROUS!!!
            for i,c in enumerate(convention[2:5]):
                if c == '+':
                    new_rock.permeability[i] = dat.grid.block[b].rocktype.permeability[i]
                    
            dat.grid.add_rocktype(new_rock)
            print ' new rocktype added: ', new_rock.name
            dat.grid.block[b].rocktype = new_rock
        else:
            dat.grid.block[b].rocktype = dat.grid.rocktype[r_name]

def update_rocktype_byname(dat, blk_names, to_rockname, configuration=None):
    """
        if need new rocktype, new one will be created from scratch,
        according to rules in configuration.  Still needs some rocktype
        to copy from, a cloest match will be search and priorities
        the leading characters.
    """
    pass

def closest_rocktype(dat, to_rockname):
    
    pass
    
def update_rocktype_property_byblocks(prop,blk_names,dat,value):
    """ attempt to update one of the property of a list of blocks (names) 
        by creating a new rocktype for them.  New rock type will be based 
        on the first block's rocktype NOTE prop is a string used directly 
        on PyTOUGH's rocktype object """
    rock = dat.grid.block[blk_names[0]].rocktype

    import copy
    new_rock = copy.deepcopy(rock)
    new_rock.name = find_unused_rocktype_name(dat,blk_names[0])
    dat.grid.add_rocktype(new_rock)
    rock = new_rock

    # prop is a string
    # if prop is 'porosity' then the line will be executed:
    #     rock.porosity = value
    exec 'rock.' + prop.strip() + ' = value'
    for b in blk_names:
        dat.grid.block[b].rocktype = rock
    
def update_rocktype_property_byblock(prop,blk_name,dat,value):
    """ attempt to update one of the property of a single block by creating 
        a new rocktype for it if necessary.  NOTE prop is a string used 
        directly on PyTOUGH's rocktype object """
    rock = dat.grid.block[blk_name].rocktype

    if dat.grid.rocktype_frequency(rock.name) > 1:
        import copy
        new_rock = copy.deepcopy(rock)
        new_rock.name = find_unused_rocktype_name(dat,blk_name)
        dat.grid.add_rocktype(new_rock)
        rock = new_rock

    # prop is a string
    # if prop is 'porosity' then the line will be executed:
    #     rock.porosity = value
    exec 'rock.' + prop.strip() + ' = value'
    dat.grid.block[blk_name].rocktype = rock
    print blk_name, 'used rocktype: ', rock.name


def find_unused_rocktype_name(dat,suggestion):
    """ increment the name sug until the name is not used by
        any other rocktype """
    all_chars = ''.join([ ' 0123456789',
        'abcdefghijklmnopqrstuvwxyz',
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ' ])
    sug = ''
    sug = suggestion
    p = 0
    s = all_chars.index(sug[p])
    n = 0
    n = s
    while dat.grid.rocktype_frequency(sug) > 0:
        n += 1
        if n > len(all_chars): n = 0
        if n == s:
            p += 1
            s = all_chars.index(sug[p])
            n = s
        if p > 4: break
        sug = sug[:p]+all_chars[n]+sug[p+1:]
    if p > 4:
        print "Error! Can't 'find_unused_rocktype_name()'"
        exit()
    return sug
