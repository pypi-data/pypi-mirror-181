# coding="utf-8"

from sgt import pilatus

if __name__ == "__main__":

    arr = pilatus.ReadTiff("test data PF/AgBh.tif")

    from matplotlib import pyplot

    pyplot.imshow(arr)

    pyplot.show()