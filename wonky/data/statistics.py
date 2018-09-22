from numba import jit
import numpy as np
import pandas as pd

class experiment_options(dict):
    pass

class statistics(np.ndarray):   
    def __new__(subtype, shape, dtype=float ):
        size = list(shape)
        size.insert(2,9)
        obj = super(statistics, subtype).__new__(subtype, size, dtype)  
        obj._num_species = size[0]
        obj._num_obs = size[1]
        obj._num_moments = size[-2]
        obj._num_increments = size[-1]
        obj._last_t = 0
        obj[:] = 0 
        obj._counter = np.zeros((obj._num_obs,obj._num_species),np.int)
        return obj

    def observable(self, obs=0, species=0):
        return pd.DataFrame(self[species][obs]).T
        
    def __init__(self, *args):
        pass
        
    def init(self):
        self[:] = 0 
        self._counter[:] = 0
        return self

    def save(self, file=None):
        np.save(file,self)
    
    @jit
    def update(self, t, v):
        self._counter += v
        self._last_t = t
        for o in range(self._num_obs):
            for s in range(self._num_species):
                for m in range(self._num_moments):   
                    self[s][o][m][t] = self._counter[o][s]**m
                
    @jit
    def flush(self):
        for o in range(self._num_obs):
            for s in range(self._num_species):
                for m in range(self._num_moments):
                    ar = self[s][o][m]
                    val = ar[self._last_t]
                    self[s][o][m][self._last_t:] = val                           
    
#stats module time loop test
#create a numpy tensor wrapper with functions and make it avaialble to another object which is itself fast

 