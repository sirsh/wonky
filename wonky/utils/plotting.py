from matplotlib import pyplot as plt
import numpy as np

#need to do the species mask filters for these objects 
#show grid lines

def display(lattice,species,dim=2):
    from matplotlib import pyplot as plt
    shape = np.zeros(dim,np.int)
    length = int(len(lattice)**(1/dim))
    shape[:] = length
    image = np.reshape(lattice,shape)
    return plt.imshow(image, "Blues")

#later refactor this into method aboive but let them diverge for now
def grid_display(lattice,species,dim=2):
    
    shape = np.zeros(dim,np.int)
    length = int(len(lattice)**(1/dim))
    shape[:] = length
    image = np.reshape(lattice,shape)
    
    canvas = np.zeros(image.shape)
    canvas[::2] = 3
    canvas[:,::2] = 3
    #mask will change to something more sophisticated based on mask
    canvas[image>0] = image[image>0]
    plt.imshow(canvas, "nipy_spectral")