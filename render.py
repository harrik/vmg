import numpy as np
import torch 
import torch.autograd as autograd 

def render_isocurves(axis, origin, target, resolution, leg_duration):

    x = np.linspace(-1.25, 1.25, resolution)
    y = np.linspace(-1.25, 1.25, resolution)
    yv, xv = np.meshgrid(y, x, indexing='ij')

    duration = np.zeros((resolution,resolution))
    first_tack_grad = np.zeros((resolution,resolution,2))

    # Calculate duration using each grid cell as the tack location
    for j in range(0,yv.shape[0]):
        for i in range(0,xv.shape[0]):
            first_tack = torch.tensor([yv[j,0]+0.0, xv[0,i]], requires_grad = False)
            dur = leg_duration(origin, first_tack, target)
            duration[j,i] = dur
            #dur.backward()
            #first_tack_grad[j,i] = (first_tack.grad).clone()

    isocurves = np.arange(-50,50,0.5)        
    
    # Display them
    keke = axis.contour(duration, isocurves, colors='k')
    axis.clabel(keke, inline=1, fontsize=20, fmt='%.1f')
    #axis.contour(first_tack_grad[:,:,0], isocurves)
    #axis.contour(first_tack_grad[:,:,1], isocurves)

# Convert from the unit circle coordinates to chart coordinates
# Returns (x,y) coordinates for drawing shapes on charts
def u2g(location, resolution):
    y = np.linspace(-1.25, 1.25, resolution)
    x = np.linspace(-1.25, 1.25, resolution)

    ny = [abs(j-location[0]) for j in y]
    idx_y = ny.index(min(ny))
    
    nx = [abs(i-location[1]) for i in x]
    idx_x = nx.index(min(nx))
    
    loc = np.array([idx_x, idx_y])
    
    return loc