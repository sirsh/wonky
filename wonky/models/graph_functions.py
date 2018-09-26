import numpy as np
from numba import jit

#list for trace, list for active flag, list for species count per site - capped, list for active particles of type
#reactions later will have a fast function that validates a reaction and then we choose one of viable by proportionate rate
def get_hyper_lattice(length,dim):
    size = length**dim
    return np.zeros(size,np.int8)

def get_species_counter(length,dim,nspecies):
    size = length**dim
    return np.zeros((size, nspecies), np.int)
    
def put (lattice,i,species):
    lattice[i] |= (1<<species)
    return lattice[i]

def remove(lattice,i,species):
    lattice[i] &= ~(1<<species)
    return lattice[i]

def get (lattice,i,species):
    return lattice[i] & (1<<species)

def __wrapped__(i, idash,length, axis,jump):
        boundary = jump * length
        if (np.floor(i/boundary)!=np.floor(idash/boundary)):  
            return int((idash + boundary) % boundary)
        return idash

def get_neighbours(i, length, dim):
    for choice in range(2*dim):
        axis = int(choice/2.)
        sense = -1 if choice % 2 == 0 else 1
        jump = length**axis
        yield __wrapped__(i, i + (sense * jump),length,axis,jump*1.)

@jit
def diffuse(i, length, dim):
    choice = np.random.randint(2*dim)
    axis = int(choice/2.)
    sense = -1 if choice % 2 == 0 else 1
    jump = length**axis
    return __wrapped__(i, i + (sense * jump),length,axis,jump*1.)

#@jit
def __coord__(i,L,D=2):
    res = np.zeros(D,np.int)
    for index, c, in enumerate(reversed(range(D))):
        res[index] = int(np.floor(i/L**c))
        i %= L**c
    return res

@jit
def walk_lattice_from(lattice, size, i=5550, walk_length=1000):
    for n in range(walk_length):
        put(lattice,i,1)
        i = diffuse(i,*size)   

#@jit
def lattice_walk_displacements(lattice, size, i=5550, walk_length=1000):
    time_disp = np.zeros(walk_length)
    init_i = i
    
    def dist(a,b):
        v1 = __coord__(a,*size)
        v2 = __coord__(b,*size)
        d =  np.sqrt((v1[0]-v2[0])**2+(v1[1]-v2[1])**2)
        return d
        
    for t, n in enumerate(range(walk_length)):
        put(lattice,i,1)
        i = diffuse(i,*size) 
        time_disp[t] = dist(i,init_i)
    return time_disp
