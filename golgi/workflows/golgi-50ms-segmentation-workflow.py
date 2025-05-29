# load libraries

from aicsimageio import AICSImage
from tifffile import imsave
from pathlib import Path
import numpy as np
from skimage.filters import threshold_otsu
from skimage.morphology import ball, binary_closing, remove_small_objects, dilation, erosion, disk
from aicssegmentation.core.pre_processing_utils import  intensity_normalization, edge_preserving_smoothing_3d
from aicssegmentation.core.vessel import vesselness3D
from aicssegmentation.core.seg_dot import dot_2d
from aicssegmentation.core.utils import topology_preserving_thinning, hole_filling
import matplotlib.pyplot as plt
from itkwidgets import view   
from aicssegmentation.core.visual import seg_fluo_side_by_side,  single_fluorescent_view, segmentation_quick_view
plt.rcParams["figure.figsize"] = [16, 12]
from aicssegmentation.core.MO_threshold import MO
import warnings
warnings.filterwarnings('ignore')

# read image
filename = "//allen/aics/microscopy/PRODUCTION/PIPELINE_8_1/5500000635_EE_1-01/aligned_split/5500000635_EE_1-01_AcquisitionBlock7_pt7_Scene-27_aligned.ome.tiff"

reader = AICSImage(filename)
IMG = reader.data.astype(np.float32)
print(IMG.shape)

# view channels
#%%
N_CHANNELS = IMG.shape[1] 
MID_SLICE = int(0.5*IMG.shape[2])

fig, ax = plt.subplots(1, N_CHANNELS, figsize=(18,16), dpi=72, facecolor='w', edgecolor='k')
if N_CHANNELS==1:
    ax.axis('off')
    ax.imshow(IMG[0,0,MID_SLICE,:,:], cmap=plt.cm.gray)
    
else:
    for channel in range(N_CHANNELS):
        ax[channel].axis('off')
        ax[channel].imshow(IMG[0,channel,MID_SLICE,:,:], cmap=plt.cm.gray)
    plt.show()

# select channel of interest
structure_channel = 1
struct_img0 = IMG[0,structure_channel,:,:,:].copy()
print(struct_img0.shape)


