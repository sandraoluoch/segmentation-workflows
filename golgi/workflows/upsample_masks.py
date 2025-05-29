from skimage.transform import rescale
import glob
import dask
import os
from skimage.io import imread, imsave

#srcdir = "//allen/aics/assay-dev/users/Sandi/emt-golgi-fov/5500000408/predictions"
srcdir = "/allen/aics/assay-dev/users/Sandi/golgi-segmentations/label-free/predictions"
destdir = "/allen/aics/assay-dev/users/Sandi/golgi-segmentations/label-free/end-results"
if not os.path.exists(destdir):
    os.mkdir(destdir)


def upsample(fn):
    img = imread(fn)
    upsampled = rescale(img, (1, 2, 2), order=0, preserve_range=True)
    imsave(fn.replace(srcdir, destdir), upsampled)


lazy_results = []
for fn in glob.glob(srcdir + "/*.tif*"):
    lazy_results.append(dask.delayed(upsample)(fn))
    #break
futures = dask.persist(*lazy_results)
dask.compute(*futures)