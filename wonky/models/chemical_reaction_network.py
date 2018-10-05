from .. import np
#import pandas as pd
from numpy.random import choice, randint
from numba import jit
from .. import statistics, lattice, reaction,plotting
from .. utils import get_paramter_space,dict_dump_to_file
from .. import settings, __version__


class crn(object):
    
    #TODO static function from_dict(d)# d containing reactions (also from d) and other bits. 
    #These would be loaded from a settings file so wrap with from_settings("filename")
    
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
        ##assume we can change the lattice size or reaction system in principle but do not do so for now
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
            if s > 0:#if there is at least one, add 
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
        plotting.grid_display(self._lattice_map,species)
        
    def display_trace(self,species=0):
        plotting.grid_display(self._trace_map,species)
        
    def lattice_sites(self):
        import pandas as pd
        return pd.DataFrame(self._lattice_sites)
    
    #####################
    ###Begin manage active sites
    #####################
    
    @property
    def active_site_count(self):return self._active_sites[-1]
    
    @staticmethod
    def __active_site_enter__(i,lattice_map, active_sites):
         #site tracking - if we are adding something for the first time, add to active sites
        if lattice_map[i] == 0:
            active_sites[active_sites[-1]] = i
            active_sites[-1] +=1
            
    @staticmethod
    def __active_site_exit__(i,lattice_map, active_sites):
        #check on visiting site if we are first
        if lattice_map[i] == 0:
            active_sites[active_sites[-2]] =  active_sites[active_sites[-1] - 1]
            active_sites[-1]-=1

    def sample_active_site(self):
        #pick any active site
        r = randint(self._active_sites[-1])
        #record which one we sampled to manage stack
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
    
    @staticmethod
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
        
    @staticmethod
    def __remove__(i,s, trace_delta, lattice_map, trace_map, lattice_sites):    
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
            #sample from the model with parameters
            self.sample(p) 
            if yield_trace: yield self._trace_map
        #dump meta data
        metafile = "./meta" if "name" not in self._options else self._options["name"]+"/meta"
        #in practice should check some os and serializability conditions. 
        dict_dump_to_file({"seed": settings.seed, "params": ex_options, "wonky_version": __version__},metafile)
       
    @staticmethod      
    @jit
    def __reaction_diffusion_sampler__(i, rsystem, lattice_sites):
        '''
        Samples from a choice of reactions - filters viable reactions based on what species or on the site
        The viable reactoin is then sampled according to it's rate
        The return value is a vector of changes for each species in the system.
        This is vector orientated contract is is useful for general reaction systems
        '''
        sys = rsystem[0]
        #only reactions for which there are sufficient particles at sites can happen
        mask = np.all((lattice_sites[i]-sys[:,:,0]  >= 0) ,axis=1)
        viable_subsystem = sys[mask]
        rates = rsystem[-1][mask]
        rates /= rates.sum()
        
        if len(rates) == 0:print("empty choice at site", i, lattice_sites[i])
        #choose a reaction from the viable subsystem according to the rates
        #in principle we could insert a void ation to norm the rates differently 
        ch = choice(len(rates),1,p=rates)[0]
        
        ch = viable_subsystem[ch]
        delta = -ch[:,0] + ch[:,1]    
        return delta#,trace delta on any site
    
    @staticmethod
    @jit
    def __update_sites__(i, delta, lattice_map, trace_map, lattice_sites, active_sites, length, dim=2):  
        '''
        This is the main method: given a delta for all species, it creates or destroys new species locally and diffuses new species
        The invoked methods understand how to interact with the lattice and update traces and various state counters
        Diffusion is delegated to the lattice function e.g. for a regular lattice
        A large part in this scope is understanding when sites are visited for the first time
        while also keeping track of the number of particles of a given type per site
        '''
        trace_delta = np.zeros(len(delta))
        for s, c in enumerate(delta):
            if c > 0:#case positive changes for species
                crn.__put__(i,s, trace_delta, lattice_map, trace_map,lattice_sites,active_sites)
                idash = lattice.diffuse(i, length, dim)
                crn.__remove__(i,s, trace_delta, lattice_map, trace_map,lattice_sites)
                crn.__put__(idash,s, trace_delta, lattice_map, trace_map,lattice_sites,active_sites) 
            if c < 0:
                crn.__remove__(i,s, trace_delta, lattice_map, trace_map,lattice_sites)    
        return trace_delta
    
    @jit
    def sample(self,params={},display=False):
        '''
        This is the main workflow entry point - sample a single realisation of a reaction-diffusion process
        no complex logic should exist here - delegate to other methods that can be unit tested
        the transaction samples a random [active] site, then samples a [viable] reaction for the site, applies the reaction and then exits the site scope.
        On exit, it is important to check if the site is still [active] and manage the active site list for further processing
        Statistics are updated using the species population and trace deltas
        Stats are flushed if there is still something 'on the clock' - All stat frames are auto-filled to the same point where necessary
        '''
        #TODO: Should add an N iterations loop here in practice but for illustration I do not. 
        #In that case we would read params["N"] and run that many instances
        #as is, we just treat N as a chunk number instead, where chunk has 1 sample
        
        
        self.__reset__(params)#reset the lattice etc. we are starting a fresh model instance
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
        #for early termination of processes fill forward for remaining t to ensure non-ragged data frames
        self.stats.flush()
        if display:self.display_trace(0)
        if "name" in params: self.stats.save(params["name"])
