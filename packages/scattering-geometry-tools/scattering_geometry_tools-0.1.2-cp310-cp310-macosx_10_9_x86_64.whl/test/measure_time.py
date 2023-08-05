# coding="utf-8"

import numpy as np
import sgt
from sgt import pilatus, _pycore
import snpl

if __name__ == "__main__":

    def do():
        u, v = sgt.make_pixel_coords_in_detector_system(1475, 1679, 0.172, 0.172, 132.35480107291554, 134.38701048529217)
        R = sgt.make_rotation_matrix(0.0, 0.0, 0.0)
        a, b, n = sgt.make_basis_vectors_on_detector_in_lab_system(R)
        x, y, z = sgt.make_pixel_coords_in_lab_system(u, v, a, b, n, 3227.5827418135564)
        qx, qy, qz = sgt.make_q(x, y, z, 1.200)

        # mask = sgt.make_default_mask(1475, 1679)
        mask = snpl.image.NpzImage("test data PF/Mask_EmptyBeam_ManuallyEdited.npz").get_layer("mask")

        map_q, map_azi, density, ax_q, ax_azi = _pycore.calc_polar_map(qx, qy, qz, mask, 0.0, 0.2, 800, 36)

        intensity = pilatus.ReadTiff("test data PF/AgBh.tif").astype(float)
        e_intensity = np.sqrt(intensity)
        e_intensity[intensity <= 0.0] = 0.0

        av, e_av = _pycore.circular_average(intensity, e_intensity, map_q, map_azi, density)

    import cProfile, pstats

    cProfile.run("do()", sort="tottime")

    # from matplotlib import pyplot
    # grid_q, grid_azi = np.meshgrid(ax_q, ax_azi)
    # pyplot.pcolormesh(grid_q, grid_azi, av, shading="nearest")
    # pyplot.show()