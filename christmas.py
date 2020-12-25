import numpy as np
import math
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def animate_scatters(iteration, data, scatters):
    for i in range(data[0].shape[0]):
        scatters[i]._offsets3d = (data[iteration][i,0:1], data[iteration][i,1:2], data[iteration][i,2:])
    return scatters

def generate_animation(data, save=False):

    # Attaching 3D axis to the figure
    fig = plt.figure(facecolor='black')
    ax = p3.Axes3D(fig)
    ax.set_facecolor('black')
    
    # remove fill
    # Get rid of the panes
    ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))

    # Get rid of the spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    
    # Set x,y,z limit for Scale
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_zlim(0, 1)
    
    # Initialize scatters
    scatters = [ 
        ax.scatter(
            data[0][i,0:1], data[0][i,1:2], data[0][i,2:], 
            marker='*', 
            color='forestgreen' if data[0][i,2:] != 1 else 'yellow'
        ) 
        for i in range(data[0].shape[0]) ]

    # Number of iterations
    iterations = len(data)
    ax.set_title('3D Christmas Tree', color='white')

    # Provide starting angle for the view.
    ax.view_init(25, 10)
    
    # remove grid
    ax.grid(False)
    
    ani = animation.FuncAnimation(fig, animate_scatters, 
                                  iterations, fargs=(data, scatters),
                                  interval=50, 
                                  blit=False, repeat=True)

    if save:
        ani.save('Merry_Christmas.gif', writer='imagemagick', fps=30)

    plt.show()

def generate_data(step):
    H =20
    data = [np.array([0, 0, 1]).reshape(1, 3)]
    for h in range(1, H+1):
        num_points = h*3
        x = np.sin(np.linspace(0+step*0.1, 2*math.pi+step*0.1, num=num_points+1))[:-1]*h/H*math.cos(abs(1-step*0.04))
        y = np.cos(np.linspace(0+step*0.1, 2*math.pi+step*0.1, num=num_points+1))[:-1]*h/H*math.cos(abs(1-step*0.04))
        z = np.full(num_points, (H-h)/H)
        data.append(np.vstack([x, y, z]).T)
    
    return np.concatenate(data)

datas = []
iters = 50
for i in range(iters):
    datas.append(generate_data(i))

data = np.stack(datas)
print(data.shape)

generate_animation(data, save=True)