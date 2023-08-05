# coding="utf-8"

from sgt import core
import numpy as np
from matplotlib import pyplot

if __name__ == "__main__":
    ax = pyplot.figure().add_subplot(projection="3d")
    ax.set_box_aspect((1,1,1))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_zlim(-1.5, 1.5)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    def plot_vector(ax, vec, **kwargs):
        return ax.plot([0.0, vec[0]], [0.0, vec[1]], [0.0, vec[2]], **kwargs)

    a, b, n = core.make_basis_vectors_on_detector_in_lab_system(core.make_rotation_matrix(0.0, 0.0, 0.0))
    
    plot_vector(ax, a, ls="-", color="r", marker="x", alpha=0.5)
    plot_vector(ax, b, ls="-", color="g", marker="x", alpha=0.5)
    plot_vector(ax, n, ls="-", color="b", marker="x", alpha=0.5)

    a, b, n = core.make_basis_vectors_on_detector_in_lab_system(core.make_rotation_matrix(10.0, 0.0, 0.0))
    
    plot_vector(ax, a, ls="-", color="r", marker="^", alpha=0.5)
    plot_vector(ax, b, ls="-", color="g", marker="^", alpha=0.5)
    plot_vector(ax, n, ls="-", color="b", marker="^", alpha=0.5)

    a, b, n = core.make_basis_vectors_on_detector_in_lab_system(core.make_rotation_matrix(10.0, 10.0, 0.0))
    
    plot_vector(ax, a, ls="-", color="r", marker="s", alpha=0.5)
    plot_vector(ax, b, ls="-", color="g", marker="s", alpha=0.5)
    plot_vector(ax, n, ls="-", color="b", marker="s", alpha=0.5)

    a, b, n = core.make_basis_vectors_on_detector_in_lab_system(core.make_rotation_matrix(10.0, 10.0, 10.0))
    
    plot_vector(ax, a, ls="-", color="r", marker="o", alpha=0.5)
    plot_vector(ax, b, ls="-", color="g", marker="o", alpha=0.5)
    plot_vector(ax, n, ls="-", color="b", marker="o", alpha=0.5)

    pyplot.show()