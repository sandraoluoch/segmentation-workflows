from skimage.transform import rescale
import glob
import dask
import os
from skimage.io import imread, imsave
import numpy as np

srcdir = "/allen/aics/assay-dev/users/Sandi/golgi-segmentations/all-raw-imgs"
destdir = "/allen/aics/assay-dev/users/Sandi/golgi-segmentations/"
# Create folders expected by EmbedSEg
for sd in [destdir, destdir + "test", destdir + "test/images/"]:
    if not os.path.exists(sd):
        os.mkdir(sd)
destdir = destdir + "test/images/"

def downsample(
    fn,
    destdir,
    bf_channel=1,
):
    img = np.squeeze(imread(fn))
    if len(img.shape) == 4:
        img = img[:, bf_channel, :, :]
    assert len(img.shape) == 3, f"{fn} has shape {img.shape}. Must be 3D"
    downsample = rescale(img, (1, 0.5, 0.5), preserve_range=True, anti_aliasing=True)
    crops = np.mod(downsample.shape, 8)

    start_crops = crops // 2
    end_crops = start_crops - crops
    end_crops += downsample.shape
    downsample = downsample[
        start_crops[0] : end_crops[0],
        start_crops[1] : end_crops[1],
        start_crops[2] : end_crops[2],
    ]
    assert (
        np.sum(np.mod(downsample.shape, 8)) == 0
    ), f"{fn} has shape {downsample.shape}"  # make sure all dims div by 8
    # imsave(fn.replace(srcdir, destdir), downsample)
    imsave(destdir + fn.split("/")[-1], downsample)
    print("Done:", fn.split("/")[-1])

# def downsample(fn):
#     img = np.squeeze(imread(fn))
#     if len(img.shape) == 4:
#         img = img[:, 1, :, :]
#     assert len(img.shape) == 3, f"{fn} has shape {img.shape}. Must be 3D"
#     downsample = rescale(img, (1, 0.5, 0.5), preserve_range=True, anti_aliasing=True)
#     crops = np.mod(downsample.shape, 8)

#     print(downsample)

#     start_crops = crops // 2
#     end_crops = start_crops - crops
#     end_crops += downsample.shape
#     downsample = downsample[
#         start_crops[0] : end_crops[0],
#         start_crops[1] : end_crops[1],
#         start_crops[2] : end_crops[2],
#     ]
#     assert (
#         np.sum(np.mod(downsample.shape, 8)) == 0
#     ), f"{fn} has shape {downsample.shape}"  # make sure all dims div by 8
#     imsave(fn.replace(srcdir, destdir), downsample)


lazy_results = []
for fn in glob.glob(srcdir + "/*.tif*"):
    lazy_results.append(dask.delayed(downsample)(fn, destdir = destdir))
    print(fn)
futures = dask.persist(*lazy_results)
dask.compute(*futures)
