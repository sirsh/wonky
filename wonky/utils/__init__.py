from glob import glob
from os import path
import numpy as np
import pandas as pd

def get_paramter_space(params):
    from itertools import product
    keys = sorted(list(params.keys()))
    
    prod = list(product(*[list(params[k]) for k in  keys]))
    l = len(prod)
    ekeys = [str(i).zfill(len(str(l))) for i in range(l)]
    import pandas as pd
    pspace = pd.DataFrame(prod,columns=keys)
    pspace["name"] = ekeys
    return pspace#.set_index("name")


def compile_statistics(  observable = 0, species =0, params = None,ename="./sample_data/exp", ext="*.npy"):
    search_path = path.join(ename, ext)
    all_data = []
    for f in glob(search_path):
        ar = np.load(f)[species][observable]
        ar = pd.DataFrame(ar).T
        ar["name"] = path.basename(f).split(".")[0]
        ar = ar.reset_index()
        all_data.append(ar.set_index("name"))
    all_data = pd.concat(all_data)
    
    if params is not None:
        pspace= get_paramter_space(params).set_index("name")
        all_data = pspace.join(all_data)
    return all_data
    