


__version__ = "0.5.0"

class _settings(dict):
    
    def __init__(self, path):
        self.path = path
        self.settings_validated = False
        self.reload()
        
    def reload(self):
        import os
        import json
        if os.path.exists(self.path):
            with open(self.path) as f:
                try:
                    data = json.load(f)
                    dict.__init__(self,data)
                except Exception as e:
                    #should report error 
                    #print(repr(e))
                    return
                self.settings_validated = True
            for k, v in data.items(): setattr(self, k, v)
                  
#could get path from os.environs but assume local settings location
settings = _settings("./settings.json")
                    
#load numpy first, which has a random number generator
import numpy as np
#choose a seed from config
if "seed" in settings: np.random.seed(int(settings["seed"]))
    
from . import models, utils, data
from .models.reaction_system import reaction
from .models import graph_functions as lattice
from .data import statistics
from .utils import plotting
from .models.chemical_reaction_network import crn