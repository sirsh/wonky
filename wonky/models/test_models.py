from . import graph_functions as gf

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

if __name__ == '__main__':
    unittest.main()    
        
