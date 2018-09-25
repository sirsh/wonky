import numpy as np
from numba import jit

#list for trace, list for active flag, list for species count per site - capped, list for active particles of type
#reactions later will have a fast function that validates a reaction and then we choose one of viable by proportionate rate
def get_hyper_lattice(lattice,dim):
    size = lattice**dim
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
    #this checks that we are on the same partition - jump should be float
    #torus: jump in the positive sense and mod by the next partition boundary

    choice = np.random.randint(2*dim)
    axis = int(choice/2.)
    sense = -1 if choice % 2 == 0 else 1
    jump = length**axis
    return __wrapped__(i, i + (sense * jump),length,axis,jump*1.)

#@jit
def walk_lattice_from(lattice, size, i=5550, walk_length=500000):
    for n in range(walk_length):
        put(lattice,i,1)
        i = diffuse(i,*size)   
