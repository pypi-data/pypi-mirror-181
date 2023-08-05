# coding="utf-8"

import sgt
from matplotlib import pyplot
import snpl

import numpy as np

if __name__ == "__main__":
    g = sgt.geometry()
    g.load_specs("test data PF/Geometry_AgBh.txt")
    g.refresh_q()

    mask = snpl.image.NpzImage("test data PF/Mask_EmptyBeam_ManuallyEdited.npz").get_layer("mask")
    i = sgt.pilatus.ReadTiff("test data PF/AgBh.tif").astype(np.float64)
    e_i = np.sqrt(i)

    g.mask = mask
    g.refresh_polar_map()

    g.save_specs("test data PF/Geometry_AgBh_saved.txt")

    g2 = sgt.geometry()
    g2.load_specs("test data PF/Geometry_AgBh_saved.txt")
    g2.mask = mask
    g2.refresh_q()
    g2.refresh_polar_map()

    av, e_av = g.circular_average(i, e_i)

    maskp = np.full_like(mask, np.nan, dtype=float)
    maskp[mask==1] = 1.0

    pyplot.pcolormesh(g.x, g.y, i, shading="nearest")
    pyplot.pcolormesh(g.x, g.y, maskp, shading="nearest", cmap="Greys", vmin=0, vmax=1)

    pyplot.gca().set_aspect("equal")

    pyplot.savefig("test_geometry.png", dpi=300)
    pyplot.cla()
    pyplot.clf()

    q, azi = np.meshgrid(g.ax_q, g.ax_azi)

    print(q)

    pyplot.pcolormesh(q, azi, av, shading="nearest", vmax=10000.0)
    pyplot.savefig("test_geometry_averaged.png", dpi=300)