from typing import List

import numpy as np
from scipy.ndimage import distance_transform_edt
from skimage.measure import label, regionprops
from skimage.morphology import ball, disk, dilation, erosion, medial_axis, remove_small_objects

import imgcorrection as icr
from PIL import Image

# load the tif image 
im = Image.open('img-test.tiff')

# convert tif image to numpy array
imarray = numpy.array(im)
print(imarray)
