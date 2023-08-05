# coding="utf-8"

import numpy as np
from sgt import crystal
from matplotlib import pyplot


if __name__ == "__main__":
    
    a = 1.5
    b = 2.0
    c = 4.0

    al = 100.0
    be = 110.0
    ga = 120.0

    avec, bvec, cvec = crystal.make_abc_vectors(a, b, c, al, be, ga)

    ax = pyplot.figure().add_subplot(projection="3d")
    ax.set_box_aspect((1,1,1))
    ax.set_xlim(-5.0, 5.0)
    ax.set_ylim(-5.0, 5.0)
    ax.set_zlim(-5.0, 5.0)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    def plot_vector(ax, vec, **kwargs):
        return ax.plot([0.0, vec[0]], [0.0, vec[1]], [0.0, vec[2]], **kwargs)
    
    print("a", np.linalg.norm(avec))
    print("b", np.linalg.norm(bvec))
    print("c", np.linalg.norm(cvec))
    print("a-b", np.rad2deg(np.arccos(np.dot(avec, bvec)/a/b)))
    print("b-c", np.rad2deg(np.arccos(np.dot(bvec, cvec)/b/c)))
    print("c-a", np.rad2deg(np.arccos(np.dot(cvec, avec)/c/a)))

    plot_vector(ax, [1.0, 0.0, 0.0], ls="-", color="r", alpha=0.5)
    plot_vector(ax, [0.0, 1.0, 0.0], ls="-", color="g", alpha=0.5)
    plot_vector(ax, [0.0, 0.0, 1.0], ls="-", color="b", alpha=0.5)

    plot_vector(ax, avec, ls="-", color="r", lw=2)
    plot_vector(ax, bvec, ls="-", color="g", lw=2)
    plot_vector(ax, cvec, ls="-", color="b", lw=2)

    pyplot.show()