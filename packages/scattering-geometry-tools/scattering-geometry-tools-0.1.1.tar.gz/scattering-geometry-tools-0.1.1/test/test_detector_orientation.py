# coding="utf-8"

from sgt import core
import numpy as np
from matplotlib import pyplot

if __name__ == "__main__":
    ax = pyplot.figure().add_subplot(projection="3d")
    ax.set_box_aspect((1,1,1))
    ax.set_xlim(-4000.0, 4000.0)
    ax.set_ylim(-4000.0, 4000.0)
    ax.set_zlim(-4000.0, 4000.0)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")



    def plot_vector(ax, vec, **kwargs):
        return ax.plot([0.0, vec[0]], [0.0, vec[1]], [0.0, vec[2]], **kwargs)

    sdd = 3193.0

    a, b, n = core.make_basis_vectors_on_detector_in_lab_system(core.make_rotation_matrix(0.0, 0.0, 0.0))
    
    u, v = core.make_pixel_coords_in_detector_system(1475, 1679, 0.172, 0.172, 128.2, 132.7)

    x, y, z = core.make_pixel_coords_in_lab_system(u, v, a, b, n, sdd)

    pyplot.plot([x[0,0], x[0,-1], x[-1,-1], x[-1,0], x[0,0]], 
                [y[0,0], y[0,-1], y[-1,-1], y[-1,0], y[0,0]], 
                [z[0,0], z[0,-1], z[-1,-1], z[-1,0], z[0,0]], 
                marker="", ls="-", color="g")

    pyplot.plot([x[0,0]], 
                [y[0,0]], 
                [z[0,0]], 
                marker="o", ls="", color="g")

    pyplot.plot([0.0, 0.0], 
                [0.0, 0.0], 
                [0.0, sdd], 
                marker="", ls="-", color="k")

    pyplot.show()