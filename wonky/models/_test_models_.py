from . import graph_functions as gf
from . chemical_reaction_network import crn
from . reaction_system import reaction

import unittest

class test_lattice_interact(unittest.TestCase):
    def test_lattice_put_get(self):
        size = (100,2)
        L = gf.get_hyper_lattice(*size)
        #add a compule of types of the 0 index site
        res = gf.put(L,0,2)
        res = gf.put(L,0,3)
        #check that the type "2" is on the site
        res = gf.get(L,0,2)
        self.assertEquals(res, (1<<2))

    def test_lattice_remove(self):
        size = (100,2)
        L = gf.get_hyper_lattice(*size)
        #add type 2
        res = gf.put(L,0,2)
        res = gf.get(L,0,2)
        #check it is there
        self.assertEquals(res, (1<<2))
        #remove it
        gf.remove(L,0,2)
        #check it is gone
        res = gf.get(L,0,2)
        self.assertEquals(res, 0)


class test_single_species_crn(unittest.TestCase):
    def test_setup(self):
        rsys =  reaction.reaction_system([reaction("A", "A+A", 0.5),
                                          reaction("A", "0", 0.5)])
        net = crn(rsys, (9,2), ICs=[1])
        
        #init conditions add one particle at center
        self.assertEquals(net.active_site_count, 1)
        self.assertEquals(net._active_sites[0], 40)
        self.assertEquals(net._lattice_map[40], 1)
        self.assertEquals(net._trace_map[40], 1)
        self.assertEquals(net._lattice_sites[40][0], 1)
        self.assertEquals(len(net._lattice_sites), 9**2)
        self.assertEquals(len(net._active_sites), 9**2+2)
        
        return net._lattice_map, net._trace_map, net._lattice_sites, net._active_sites, net._trace_delta_template

    def test_delta_rsys(self):
        rsys =  reaction.reaction_system([reaction("A", "A+A", 0.5),
                                          reaction("A", "0", 0.5)])
        net = crn(rsys, (9,2), ICs=[1])
        delta = crn.__reaction_diffusion_sampler__(40,rsys, net._lattice_sites)  
        #there must be a positive or negative change for the species 
        self.assertEquals(abs(delta[0]), 1)   

        #we could check some other cases here too e.g. no changes if there are no viables                           

    def test_lattice_put_states(self):
        site = 40
        species = 0
        lattice, trace, sites, active_sites,trace_delta = self.test_setup()
        trace_delta[:] = 0
        before = sites[site][species]
        crn.__put__(site,species, trace_delta, lattice, trace, sites,active_sites)
        #confirm the trace on the site does not change but the number of species does
        self.assertEquals(trace_delta[species], 0)
        self.assertEquals(sites[site][species], before + 1)
        #for new site, confirm the trace and lattice site change
        site = site+1
        #trace_delta[:] = 0
        before = sites[site][species]
        crn.__put__(site,species, trace_delta, lattice, trace, sites,active_sites)
        self.assertEquals(trace_delta[species], 1)
        self.assertEquals(sites[site][species], 1)
        self.assertNotEquals(lattice[site], 0)
        
    def test_state_put(self):
        site = 40
        species = 0
        lattice, trace, sites, active_sites,trace_delta = self.test_setup()
        trace_delta[:] = 0
        delta = trace_delta.copy()
        delta[0] = 1
        trace_delta = crn.__update_sites__(site,delta, lattice, trace, sites, active_sites,9)
        #should still be one particle at the current site
        self.assertEquals(sites[site][species], 1)
        #one of the nghs 39,41,31,49 should have one more
        nghs = 0
        for ngh in [39,41,31,49]:   nghs+= sites[ngh][species] 
        self.assertEquals(nghs, 1)
        # total trace should be two in this species=0 case where the bit set is the first 1
        self.assertEquals(trace.sum(), 2)
    
    def test_state_remove(self):
        site = 40
        species = 0
        lattice, trace, sites, active_sites,trace_delta = self.test_setup()
        trace_delta[:] = 0
        delta = trace_delta.copy()
        delta[0] = -1
        trace_delta = crn.__update_sites__(site,delta, lattice, trace, sites, active_sites,9)
        #should be no particle at the current site
        self.assertEquals(sites[site][species], 0)
        self.assertEquals(lattice[site], 0)
        #should be a trace of the particle - for species 0 suffices to check first bit set and int=1
        self.assertEquals(trace[site], 1)
        #all of the nghs 39,41,31,49 should have zero
        nghs = 0
        for ngh in [39,41,31,49]:   nghs+= sites[ngh][species] 
        self.assertEquals(nghs, 0)
        # total trace should be one in this species=0 case where the bit set is the first one
        self.assertEquals(trace.sum(), 1)

    #TODO - multi species tests

if __name__ == '__main__':
    unittest.main()    
        
