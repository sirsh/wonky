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
    
def plot_many(images, size, species=0, names=[]):
    def display(lattice,species,ax, dim=2):
        from matplotlib import pyplot as plt
        shape = np.zeros(dim,np.int)
        length = int(len(lattice)**(1/dim))
        shape[:] = length
        image = np.reshape(lattice,shape)
        ax.imshow(image, "Blues")
        ax.set_xticks(np.arange(0, length, 1));
        ax.set_yticks(np.arange(0, length, 1));
        ax.set_xticklabels([]);
        ax.set_yticklabels([]);
        ax.grid(which='both',linestyle='-', linewidth='0.1', color='red')
    fig, axs = plt.subplots(*size, figsize=(10, 8))

    for i ,ax in enumerate(axs.flat):
        display(images[i],species,ax)
        ax.set_title(str(i))

    plt.tight_layout()
    plt.grid(True)