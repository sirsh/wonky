#list for trace, list for active flag, list for species count per site - capped, list for active particles of type
#reactions later will have a fast function that validates a reaction and then we choose one of viable by proportionate rate
import numpy as  np
#import pandas as pd
from numba import jit
from .. import statistics, lattice, reaction,plotting
from .. utils import get_paramter_space

class crn(object):
    def __init__(self,reaction_system, lattice_size, ICs = [], options={"name": "./sample_data/exp"}):
        self._num_species = len(reaction_system[1])
        self._rsys = reaction_system
        self._lattice_size = lattice_size
        self._ics = ICs
        self._max_time_units = 20# from options
        #keep track of static lengths so we do not have to re-compute them L * D * S
        self._dimensions = np.array(list(lattice_size)+[self._num_species])
        self._options = options
        num_observables, num_increments = 2,self._max_time_units
        self.stats =  statistics((self._num_species,num_observables,num_increments))     
        self.__reset__()
                  
    def __reset__(self,params={}):
        ##asume we can change the lattice size or reaction system in principle but do not do so for now
        self._lattice_map = lattice.get_hyper_lattice(*self._lattice_size)
        self._trace_map = lattice.get_hyper_lattice(*self._lattice_size)
        self._lattice_sites = lattice.get_species_counter(*self._lattice_size,self._num_species)  
        self._trace_delta_template = np.zeros((self._num_species))
        #for performance/simplicity we cheat with the data structure - last two locations are for meta data, count and last-sampled-address
        self._active_sites = np.zeros(len(self._trace_map)+2,np.int)  
        site = int(len(self._lattice_sites)/2)
        self.stats.init()
        self._t = 0 
        for i,s in enumerate(self._ics):
            self.put(site,i)
            #put as many species as we init with on this site
            self._lattice_sites[site][i] = s

        #update the stats for initial conditions
        self.stats.update(self._t, np.array([self._ics, self._ics],np.int))
        self._t = 1 
        
    def __repr__(self):
        return "{} species, {} reactions on a {} lattice".format(self._num_species,len(self._rsys[-1]),self._lattice_size)
       
    #for these maybe i can do multi species in a grid of subplots
    def display_lattice(self,species=0):
        species = 0
        plotting.grid_display(self._lattice_map,0)
        
    def display_trace(self,species=0):
        species = 0
        plotting.grid_display(self._trace_map,0)
        
    def lattice_sites(self):
        import pandas as pd
        return pd.DataFrame(self._lattice_sites)
    
    #####################
    ###Begin manage active sites
    #####################
    
    @property
    def active_site_count(self):return self._active_sites[-1]
    
    def __active_site_enter__(i,lattice_map, active_sites):
         #site tracking - if we are adding something for the first time, add to active sites
        if lattice_map[i] == 0:
            active_sites[active_sites[-1]] = i
            active_sites[-1] +=1
            
    def __active_site_exit__(i,lattice_map, active_sites):
        #check on visiting site if we are first
        if lattice_map[i] == 0:
            active_sites[active_sites[-2]] =  active_sites[active_sites[-1] - 1]
            active_sites[-1]-=1

    def sample_active_site(self):
        #pick any active site
        r = np.random.randint(self._active_sites[-1])
        #record wich one we sampled to manage stack
        self._active_sites[-2] = r
        return self._active_sites[r]
    
    #####################
    ###End manage active sites
    #####################
    
    #####################
    ###Begin graph interaction
    #####################
    
    def put(self,i,s):
        self._trace_delta_template[:] = 0     
        crn.__put__(i,s,self._trace_delta_template, self._lattice_map, self._trace_map, self._lattice_sites, self._active_sites)
        return self._trace_delta_template
        
    def __put__(i,s, trace_delta, lattice_map, trace_map, lattice_sites,active_sites): 
        #puts will mostly be from diffusing to another site but sometimes reactions will put items on existing sites - optimize?
        crn.__active_site_enter__(i,lattice_map, active_sites)
        lattice.put(lattice_map, i, s)
        lattice_sites[i][s]+=1
        if lattice.get(trace_map, i, s) == 0:
            lattice.put(trace_map, i, s)
            trace_delta[s]+=1
        
    def remove(self,i,s):
        d = crn.__remove__(i,s,self._trace_delta_template,self._lattice_map, self._trace_map, self._lattice_sites)
        return d
        
    def __remove__(i,s, trace_delta, lattice_map, trace_map, lattice_sites,active_sites):    
        if lattice.get(lattice_map, i, s) != 0:#check if exists  
            lattice_sites[i][s] -= 1 #decrement
            if lattice_sites[i][s] == 0: #if i am the last of my kind, remove flag
                lattice.remove(lattice_map, i, s)
            return 1
        return 0
    
    #####################
    ###End graph interaction
    #####################

    #####################
    ###Primary CRN functions
    #####################

     #todo other versions e.g. statisitcs could construct new crns - keep in mind some parameters dont require re-new
    @jit
    def run_experiment(self, ex_options,yield_trace=False):
        for k,p in get_paramter_space(ex_options).iterrows(): 
            name = str(k) if "name" not in p else p["name"]
            #update the qualified name
            p["name"] = name if "name" not in self._options else self._options["name"]+"/"+name
            res = self.sample(p) 
            if yield_trace:
                yield self._trace_map
                
    @jit
    def __reaction_diffusion_sampler__(i, rsystem, lattice_sites):
        sys = rsystem[0]
        #only reactions for which there are sufficient particles at sites can happen
        mask = np.all((lattice_sites[i]-sys[:,:,0]  >= 0) ,axis=1)
        viable_subsystem = sys[mask]
        rates = rsystem[-1][mask]
        rates /= rates.sum()
        #choose a reaction from the viable subsystem according to the rates
        choice = np.random.choice(len(rates),1,p=rates)[0]
        choice = viable_subsystem[choice]
        delta = -choice[:,0] + choice[:,1]    
        return delta#,trace delta on any site
    
    @jit
    def __update_sites__(i, delta, lattice_map, trace_map, lattice_sites, active_sites, length, dim=2):  
        trace_delta = np.zeros(len(delta))
        lattice_site = lattice_sites[i]
        for s, c in enumerate(delta):
            if c > 0:#case positive changes for species
                crn.__put__(i,s, trace_delta, lattice_map, trace_map,lattice_sites,active_sites)
                idash = lattice.diffuse(i, length, dim)
                crn.__remove__(i,s, trace_delta, lattice_map, trace_map,lattice_sites,active_sites)
                crn.__put__(idash,s, trace_delta, lattice_map, trace_map,lattice_sites,active_sites) 
            if c < 0:
                crn.__remove__(i,s, trace_delta, lattice_map, trace_map,lattice_sites,active_sites)    
        return trace_delta
    
    @jit
    def sample(self,params={},display=False):
        self.__reset__(params)
        while self._t < self._max_time_units and self.active_site_count > 0:         
            i = self.sample_active_site()
            delta = crn.__reaction_diffusion_sampler__(i,self._rsys, self._lattice_sites)
            trace_delta = crn.__update_sites__(i,delta, 
                                               self._lattice_map, 
                                               self._trace_map, 
                                               self._lattice_sites, 
                                               self._active_sites,
                                               self._lattice_size[0]
                                              )
            crn.__active_site_exit__(i, self._lattice_map,self._active_sites)
            self.stats.update(self._t, np.array([delta, trace_delta],np.int))
            self._t += 1
        #for early termination of processes fill forward for remaining t for non-ragged data frames
        self.stats.flush()
        if display:self.display_trace(0)
        if "name" in params: self.stats.save(params["name"])
